import io
import json
import base64
import enum
from typing import Dict, List, Optional, Union
from PIL import Image
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration, AutoModelForCausalLM, Qwen2VLForConditionalGeneration
from prompt import parse_and_reconstruct_fields, get_prompt
from typing import Dict, Any

class SupportedModels(enum.Enum):
    LLAVA_13B = "llava-hf/llava-1.5-13b-hf"
    LLAVA_7B = "llava-hf/llava-1.5-7b-hf"
    DEEPSEEK_VL_7B = "deepseek-ai/deepseek-vl-7b-chat"
    JANUS_PRO_7B = "deepseek-ai/Janus-Pro-7B"
    QWEN_VL_7B = "Qwen/Qwen2-VL-7B-Instruct"

class HuggingFaceModelE2E:
    def __init__(self, model_name: Union[str, SupportedModels], draw_grid: bool = False, cache_dir: Optional[str] = None):
        """
        Initialize the HuggingFace model for document processing.
        
        Args:
            model_name: Model identifier or SupportedModels enum value
            draw_grid: Whether to overlay a grid on the document image
            cache_dir: Directory to cache model files (optional)
        """
        if isinstance(model_name, SupportedModels):
            self.model_name = model_name.value
            self.model_type = model_name
        else:
            self.model_name = model_name
            # Try to match string to enum
            for model_type in SupportedModels:
                if model_type.value == model_name:
                    self.model_type = model_type
                    break
            else:
                raise ValueError(f"Unsupported model: {model_name}")
        
        self.draw_grid = draw_grid
        self.cache_dir = cache_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize appropriate model based on enum value
        if self.model_type in [SupportedModels.LLAVA_13B, SupportedModels.LLAVA_7B]:
            self.dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            self.model = LlavaForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype=self.dtype,
                low_cpu_mem_usage=True,
                cache_dir=self.cache_dir,
            ).to(self.device)
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            
        elif self.model_type in [SupportedModels.DEEPSEEK_VL_7B, SupportedModels.JANUS_PRO_7B]:
            # Import DeepSeek specific modules
            from deepseek_vl.models import VLChatProcessor, MultiModalityCausalLM
            from deepseek_vl.utils.io import load_pil_images
            
            self.dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
            self.processor = VLChatProcessor.from_pretrained(self.model_name)
            self.tokenizer = self.processor.tokenizer
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name, 
                trust_remote_code=True
            )
            self.model = self.model.to(self.dtype).to(self.device).eval()
            self.load_pil_images = load_pil_images
            
        elif self.model_type == SupportedModels.QWEN_VL_7B:
            self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                self.model_name,
                device_map="auto",
                load_in_8bit=True,
                cache_dir=self.cache_dir,       
            )
            self.processor = AutoProcessor.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
            )
    
    def add_grid_overlay(self, image):
        """Add a grid overlay to the image."""
        # Implement the grid overlay logic here
        # This is a placeholder - replace with actual implementation
        return image
    
    def encode_image_base64(self, image_path):
        """
        Encode image to base64 string.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    def forward(self, doc_image_path: str, max_new_tokens: int = 2000) -> Dict[str, Any]:
        """
        Process the document image with the specified prompt.
        
        Args:
            prompt: Text prompt for the model
            doc_image_path: Path to the document image
            max_new_tokens: Maximum number of tokens to generate
            
        Returns:
            List of dictionaries containing the parsed results
        """
        # Get prompt
        prompt = get_prompt(doc_image_path)

        # Read and potentially modify the image
        img = Image.open(doc_image_path)
        if self.draw_grid:
            img = self.add_grid_overlay(img)
        
        # Process based on model type enum
        if self.model_type in [SupportedModels.LLAVA_13B, SupportedModels.LLAVA_7B]:
            return self._forward_llava(prompt, img, max_new_tokens)
            
        elif self.model_type in [SupportedModels.DEEPSEEK_VL_7B, SupportedModels.JANUS_PRO_7B]:
            return self._forward_deepseek(prompt, img, doc_image_path, max_new_tokens)
            
        elif self.model_type == SupportedModels.QWEN_VL_7B:
            return self._forward_qwen(prompt, doc_image_path, max_new_tokens)
    
    def _forward_llava(self, prompt: str, img: Image.Image, max_new_tokens: int) -> Dict[str, Any]:
        """LLAVA models forward implementation."""
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image"},
                ],
            },
        ]
        
        model_prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = self.processor(images=img, text=model_prompt, return_tensors='pt').to(self.device)
        
        output = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        raw_response = self.processor.decode(output[0][2:], skip_special_tokens=True)
        
        # Parse the response to get the structured output
        parsed_response = self.parse_and_reconstruct_fields(raw_response)
        return parsed_response
    
    def _forward_deepseek(self, prompt: str, img: Image.Image, doc_image_path: str, max_new_tokens: int) -> Dict[str, Any]:
        """DeepSeek models forward implementation."""
        conversation = [
            {
                "role": "User",
                "content": f"{prompt}",
                "images": [doc_image_path]
            },
            {
                "role": "Assistant",
                "content": ""
            }
        ]
        
        # Load images and prepare for inputs
        pil_images = self.load_pil_images(conversation)
        prepare_inputs = self.processor(
            conversations=conversation,
            images=pil_images,
            force_batchify=True
        ).to(self.device)
        
        # Run image encoder to get the image embeddings
        inputs_embeds = self.model.prepare_inputs_embeds(**prepare_inputs)
        
        # Run the model to get the response
        outputs = self.model.language_model.generate(
            inputs_embeds=inputs_embeds,
            attention_mask=prepare_inputs.attention_mask,
            pad_token_id=self.tokenizer.eos_token_id,
            bos_token_id=self.tokenizer.bos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            use_cache=True
        )
        
        model_raw_response = self.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
        
        # Parse the response to get the structured output
        parsed_response = self.parse_and_reconstruct_fields(model_raw_response)
        return parsed_response
        
    def _forward_qwen(self, prompt: str, doc_image_path: str, max_new_tokens: int) -> Dict[str, Any]:
        """Qwen VL models forward implementation."""
        # Encode image to base64
        base64_image = self.encode_image_base64(doc_image_path)
        
        conversation = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "url": f"data:image/png;base64,{base64_image}"
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        
        inputs = self.processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)
        
        output_ids = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
        raw_response = self.processor.batch_decode(
            generated_ids, 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=True
        )[0]
        
        # Parse the response to get the structured output
        parsed_response = self.parse_and_reconstruct_fields(raw_response)
        return parsed_response
    
    def parse_and_reconstruct_fields(self, text: str) -> Dict[str, Any]:
        parsed_response = parse_and_reconstruct_fields(text)
        return parsed_response
    
        """
        Parse the model output text and reconstruct fields.
        This is a placeholder - implement the actual parsing logic.
        """
        try:
            # Simple JSON parsing for now
            # You should replace this with the actual implementation from your prompt.py
            start_idx = text.find("{")
            end_idx = text.rfind("}") + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            return [{"error": "Could not parse JSON from response"}]
        except json.JSONDecodeError:
            return [{"error": "Invalid JSON in response"}]


# Example usage
if __name__ == "__main__":
    # Using enum
    model_name = SupportedModels.DEEPSEEK_VL_7B

    model = HuggingFaceModelE2E(
        model_name=model_name,
        draw_grid=True,
        cache_dir='/local/data/rds_hf_cache'
    )
    
    result = model.forward(
        # prompt="Describe the content of this document.",
        doc_image_path="./processed_pngs/grid_al_1_page_1.png"
    )
    
    output_filename = "output_" + model_name.value.replace('/', '_').replace('.', '_') + "_parsed.txt"

    final_result = json.dumps(result, indent=2)

    with open(output_filename, "w") as f:
        f.write(final_result)
    
    print(final_result)
import os
import re
from typing import List, Dict, Tuple

import pymupdf
from PIL import Image

class GUIModel:
    def __init__(self, model_name, batch_size, file_ids, output_dir: str = "gui_agents/outputs", user_idx: int = 0):
        '''
        Initialize the GUIModel with the model name and output directory.
        
        Args:
            model_name (str): Name of the model.
            file_ids (list[str]): Filename of the PDF to extract text from.
            output_dir (str): Directory to save the output.
        '''
        self.model_name = model_name
        self.batch_size = batch_size
        self.output_dir = output_dir
        self.count = 0
        
        pdfs_dir = os.listdir(os.path.join(output_dir, model_name))
        
        self.scripts = {}
        for fid in file_ids:
            pdf_output = list(filter(lambda f: re.match(f'^{fid}-.*_sm_p{user_idx}_.*\\.pdf$', f), pdfs_dir))[0]
            print("Extracting script from PDF:", pdf_output)
        
            # for al_0_0-ccu_sm_p0_5m.pdf
            self.scripts[fid] = GUIModel.pdf_extract_text(os.path.join(output_dir, model_name, pdf_output))

        pass
        # for al_0_0.pdf
        # self.script = GUIModel.pdf_extract_text(os.path.join(output_dir, model_name, f'{filename}.pdf'))
        
    # @add_bbox
    def forward(
        self,
        nl_profile: List[str],
        doc_image: List[Image.Image],
        available_actions: List[str],
        flow: List[str],
        targets: List[str] = [],
        feedback: List[List] = None,
        suggest_localizer: bool = False,
        source_doc_image: str = None,
        file_ids: List[str] = None,
    ) -> List[Dict]:
        preds = []
        for fid in file_ids:
            script = self.scripts[fid]
            if self.count >= len(script):
                # todo: terminate and check for errors
                # raise StopIteration
                preds.append(
                    [
                        {
                            "action": "Terminate",
                        }
                    ]
                )
            else:
                preds.append([script[self.count]])
        self.count += 1

        return preds

    @staticmethod
    def pdf_extract_text(pdf_path: str, page_number: int=0, distance_threshold=5) -> List[Dict]:
        '''
        Extract text from a PDF file and convert it into Action script.
        
        Args:
            pdf_path (str): Path to the PDF file.
            page_number (int): Page number to extract text from.
            distance_threshold (int): Maximum distance to consider words as part of the same block.
            
        Returns:
            str: Action script as a string.
        '''
        doc: pymupdf.Document = pymupdf.open(pdf_path)
        page: pymupdf.Page = doc.load_page(page_number)
        width, height = page.rect.width, page.rect.height
        
        # Extract text from the page
        # (x0, y0, x1, y1, "word", word_no, block_type)
        words = page.get_text("words")
        
        doc.close()
        
        # Combine words into blocks corresponding to each "answer"
        word_blocks = GUIModel.combine_words_into_blocks(words, distance_threshold)
        
        # Convert answer blocks into Action script
        script = []
        for (x0, y0, x1, y1, text) in word_blocks:
            script.append(
                {
                    "action": "PlaceText",
                    "cx": (x0 + x1) / 2 / width,
                    "cy": (y0 + y1) / 2 / height,
                    "value": text,
                }
            )
            
        # Add a termination action at the end
        script.append(
            {
                "action": "Terminate",
            }
        )
        
        return script
    
    @staticmethod
    def combine_words_into_blocks(words, distance_threshold=5) -> List[Tuple[int, int, int, int, str]]:
        '''
        Combine words into blocks based on their proximity.
        
        Args:
            words (list): List of words with their coordinates and text.
            distance_threshold (int): Maximum distance to consider words as part of the same block.
            
        Returns:
            list: List of combined blocks with their coordinates and text.
        '''
        result_blocks = []
        current_block = []

        def calculate_distance(word1, word2):
            # Calculate Manhattan distance between the edges of two words
            x0_1, y0_1, x1_1, y1_1, *_ = word1
            x0_2, y0_2, x1_2, y1_2, *_ = word2

            horizontal_distance = max(0, x0_2 - x1_1, x0_1 - x1_2)
            vertical_distance = max(0, y0_2 - y1_1, y0_1 - y1_2)

            return horizontal_distance + vertical_distance
            
        # Sort words by their y-coordinate (top to bottom) and then by x-coordinate (left to right)
        for word in words:
            if not current_block:
                current_block = list(word[:5])
            else:
                if calculate_distance(current_block, word) <= distance_threshold:
                    current_block[4] += f" {word[4]}"
                    current_block[:4] = [
                        min(current_block[0], word[0]), 
                        min(current_block[1], word[1]), 
                        max(current_block[2], word[2]), 
                        max(current_block[3], word[3])
                    ]
                else:
                    result_blocks.append(tuple(current_block))
                    current_block = list(word[:5])
            
        # # Add the last block if it exists
        
        # # Combine words in each block into a single string
        # for i, block in enumerate(combined_blocks):
        #     # Combine text in the block
        #     combined_text = block[4]
            
        #     # combine coordinates
        #     x0 = min(word[0] for word in block)
        #     y0 = min(word[1] for word in block)
        #     x1 = max(word[2] for word in block)
        #     y1 = max(word[3] for word in block)
            
        #     # Update the block with combined coordinates and text
        #     result_blocks.append((x0, y0, x1, y1, combined_text))

        return result_blocks


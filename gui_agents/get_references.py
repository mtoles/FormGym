import user_features
import annotations
from doc_state import DocState
from utils import ProfileSourceEnum
import argparse
from PIL import Image
import inspect
import re
from fields import FieldMeta


def get_relevant_user_features(doc_state: DocState) -> set:
    def _get_referenced_features(src_code: str) -> set:
        feat_pattern = r"feat\.([A-Za-z0-9_]+)"
        feat_matches = re.findall(feat_pattern, src_code)
        other_pattern = r"user_profile\.features\.([A-Za-z0-9_]+)"
        other_matches = re.findall(other_pattern, src_code)
        get_profile_info_pattern = r"([A-Za-z0-9_]+)\.get_profile_info"

        rec_matches = []
        get_profile_info_matches = re.findall(get_profile_info_pattern, src_code)
        for match in get_profile_info_matches:
            rec_matches.extend(_get_referenced_features(inspect.getsource(FieldMeta.registry[match])))
        return set(feat_matches + other_matches + rec_matches)

    referenced_features = set()
    for field in doc_state.fields:
        field_cls = field["field"]
        src_code = inspect.getsource(field_cls)
        referenced_features_in_field = _get_referenced_features(src_code)
        assert referenced_features_in_field, f"No features referenced in {field_cls}"
        referenced_features.update(referenced_features_in_field)

    return referenced_features


def get_completed_source_doc(source_doc_id: str):
    # Load the document image and annotations
    png_path = f"pngs/{source_doc_id}.png"
    blank_img = Image.open(png_path).convert("RGB")
    annot_path = f"annotations/{source_doc_id}.json"
    annots = annotations.read_annotations(annot_path)

    # Create document state
    doc_state = DocState(annots, blank_img=blank_img, doc_id=source_doc_id)
    source_doc_relevant_user_features = get_relevant_user_features(doc_state)

    # Get relevant user features and create user profile
    source_doc_relevant_user_features = get_relevant_user_features(doc_state)

    return source_doc_relevant_user_features

def get_nl_profile(fid: str, user_idx: int, profile_source: str):
    # Validate the task argument
    profile_source = ProfileSourceEnum(profile_source).value
    
    # Prepare list to collect per-file data for batch processing
    all_files = []
    
    if "al" not in fid:
        assert profile_source == ProfileSourceEnum.TEXT.value, "Only auto loan docs dataset supports document transfer setting"
    source_doc_no = (int(fid.split("_")[1]) - 1) % 4 # use the previous doc as the source doc
    source_doc_id = f"al_{source_doc_no}_0"
    png_path = f"pngs/{fid}.png"

    blank_img = Image.open(png_path).convert("RGB")
    annot_path = f"annotations/{fid}.json"
    annots = annotations.read_annotations(annot_path)
    doc_state = DocState(annots, blank_img=blank_img, doc_id=fid)

    relevant_user_features = get_relevant_user_features(doc_state)

    user_profile = user_features.UserProfile(user_idx, relevant_user_features)
    if profile_source == ProfileSourceEnum.TEXT.value:
        nl_profile = "\n".join(user_profile.get_nl_profile())
    else:
        assert fid.startswith(
            "al_"
        ), "Only auto loan docs dataset supports document transfer setting"
        # nl_profile = "<Refer to the source image for information on the user>"
        source_doc_relevant_user_features = get_completed_source_doc(source_doc_id)
        user_features_not_in_source_doc = relevant_user_features - source_doc_relevant_user_features

        nl_user_profile = user_features.UserProfile(user_idx, user_features_not_in_source_doc)
        nl_profile = "\n".join(nl_user_profile.get_nl_profile()) if user_features_not_in_source_doc else "<Refer to the source image for information on the user>"
        
    return nl_profile

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # New argument to take a list of PNG file paths
    parser.add_argument(
        "--file_id", type=str, help="File ids, e.g. al_0_0"
    )
    # parser.add_argument("--source_doc_id", type=str, default=None)
    parser.add_argument("--user_idx", type=int, default=0)
    parser.add_argument(
        "--profile_source",
        type=str,
        help=f"Whether to use a baseline action set or our model [{', '.join([c.value for c in ProfileSourceEnum])}]",
        default=ProfileSourceEnum.TEXT.value,
    )
    args = parser.parse_args()

    print( "=" * 50)
    print(f"{get_nl_profile(args.file_id, args.user_idx, args.profile_source)}")
    print( "=" * 50)
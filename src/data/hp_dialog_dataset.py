import json


def process_dataset():
    processed_dataset = []
    new_entry = {"id": None, "scene": None, "dialogue": None, "harry_response": None}
    # Train Set
    with open("data/external/en_train_set.json", "r") as file:
        train_json = json.load(file)
        for attribute, value in train_json.items():
            for inner_attribute, inner_value in value.items():
                if inner_attribute == "speakers":
                    if "Harry" in inner_value:
                        new_entry["id"] = attribute
                if new_entry["id"] is not None and inner_attribute == "scene":
                    for scene_part in inner_value:
                        if new_entry["scene"] is not None:
                            new_entry["scene"] += scene_part
                        else:
                            new_entry["scene"] = scene_part
                if new_entry["scene"] is not None and inner_attribute == "dialogue":
                    for dialogue in inner_value:
                        if "Harry:" not in dialogue:
                            if new_entry["dialogue"] is not None:
                                new_entry["dialogue"] += dialogue
                            else:
                                new_entry["dialogue"] = dialogue
                        else:
                            harry_dialogue_without_person = dialogue.replace("Harry: ", "")
                            new_entry["harry_response"] = harry_dialogue_without_person
                            break
            if (
                new_entry["id"] is not None
                and new_entry["scene"] is not None
                and new_entry["dialogue"] is not None
                and new_entry["harry_response"] is not None
            ):
                processed_dataset.append(
                    {
                        "id": new_entry["id"],
                        "scene": new_entry["scene"],
                        "dialogue": new_entry["dialogue"],
                        "harry_response": new_entry["harry_response"],
                    }
                )
            new_entry["id"] = None
            new_entry["scene"] = None
            new_entry["dialogue"] = None
            new_entry["harry_response"] = None
    with open("data/processed/train_harry_dataset.json", "w") as outfile:
        json.dump(processed_dataset, outfile, sort_keys=False, indent=4, ensure_ascii=False)
    processed_dataset = []
    # Evaluation Set
    with open("data/external/en_test_set.json", "r") as file:
        test_json = json.load(file)
        for attribute, value in test_json.items():
            for inner_attribute, inner_value in value.items():
                if inner_attribute == "speakers":
                    if "Harry" in inner_value:
                        new_entry["id"] = attribute
                if new_entry["id"] is not None and inner_attribute == "scene":
                    for scene_part in inner_value:
                        if new_entry["scene"] is not None:
                            new_entry["scene"] += scene_part
                        else:
                            new_entry["scene"] = scene_part
                if new_entry["scene"] is not None and inner_attribute == "dialogue":
                    for dialogue in inner_value:
                        if new_entry["dialogue"] is not None:
                            new_entry["dialogue"] += dialogue
                        else:
                            new_entry["dialogue"] = dialogue
                if new_entry["dialogue"] is not None and inner_attribute == "positive_response":
                    new_entry["harry_response"] = inner_value
            if (
                new_entry["id"] is not None
                and new_entry["scene"] is not None
                and new_entry["dialogue"] is not None
                and new_entry["harry_response"] is not None
            ):
                processed_dataset.append(
                    {
                        "id": new_entry["id"],
                        "scene": new_entry["scene"],
                        "dialogue": new_entry["dialogue"],
                        "harry_response": new_entry["harry_response"],
                    }
                )
            new_entry["id"] = None
            new_entry["scene"] = None
            new_entry["dialogue"] = None
            new_entry["harry_response"] = None
    with open("data/processed/eval_harry_dataset.json", "w") as outfile:
        json.dump(processed_dataset, outfile, sort_keys=False, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    process_dataset()

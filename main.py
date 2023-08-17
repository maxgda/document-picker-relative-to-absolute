import json
from src.get_data import export
from src.process import batch_component_config_to_absolute, to_absolute, get_all_relative_pickers
from src.save import export_to_file, import_to_cms
from src.user_input import get_yes_no_input, get_execute_script_input


def main():
    file = export()

    matching_components = get_all_relative_pickers()

    if get_yes_no_input("Do you want to batch update component configuration to relative: false?"):
        batch_component_config_to_absolute(matching_components)

    get_execute_script_input("press ENTER to execute")
    modified_ndjson = process_to_absolute(file, matching_components)

    if get_yes_no_input("export modified json to file?"):
        export_to_file(modified_ndjson)

    if get_yes_no_input("import modified json to cms project?"):
        import_to_cms(modified_ndjson)


def process_to_absolute(file, matching_components):
    modified_ndjson = []
    for line in file:
        page = json.loads(line)
        modified_page = to_absolute(page, matching_components)
        modified_ndjson.append(modified_page)
    return modified_ndjson


if __name__ == "__main__":
    main()

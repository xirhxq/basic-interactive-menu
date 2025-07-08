from interactive_menu import InteractiveMenu

class A:
    def __init__(self, **kwargs):
        print(f'Class A with {kwargs}')

class B:
    def __init__(self, **kwargs):
        print(f'Class B with {kwargs}')

class C:
    def __init__(self, **kwargs):
        print(f'Class C with {kwargs}')

def main():
    all_results = (
        InteractiveMenu()
        .add_option("data1.csv")
        .add_option("data2.json")
        .add_option("data3.txt")
        .ask("Select a Data File", "file")
        .add_option("A")
        .add_option("B")
        .add_option("C")
        .ask("Select a Class", "class_name")
        .add_options(["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"])
        .allow_multiple()
        .ask("Select Chart Types", "chart_type_list")
        .get_all_results()
    )
    if all_results is None:
        print("Quit...")
        return
    cls = globals()[all_results["class_name"]]
    instance = cls(file=all_results["file"], types=all_results["chart_type_list"])
    print(f"\nYou selected: {all_results['file']}")

if __name__ == "__main__":
    main()
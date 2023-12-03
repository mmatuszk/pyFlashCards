# Import the AutoCorr class
from AutoCorr import AutoCorr

def test_auto_corr_save_load():
    # Create an instance of AutoCorr and generate test data
    auto_corr = AutoCorr()
    auto_corr.GenerateTestData()

    # Add custom autocorrection items
    auto_corr.InsertItem("example", "EXAMPLE")

    # Save the current state to a file
    save_filename = "test_autocorr_save.xml"
    auto_corr.Save(save_filename)

    # Create a new instance of AutoCorr for loading
    auto_corr_load = AutoCorr()

    # Load the data from the file
    auto_corr_load.Load(save_filename)

    # Print lists from both instances to verify they match
    print("Original AutoCorr List:")
    auto_corr.PrintList()

    print("\nLoaded AutoCorr List:")
    auto_corr_load.PrintList()

    # Additional checks can be performed here to compare individual items
    # between auto_corr and auto_corr_load if needed

# Execute the test function
if __name__ == "__main__":
    test_auto_corr_save_load()

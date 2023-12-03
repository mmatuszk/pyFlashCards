# Import the AutoCorr class
from AutoCorr import AutoCorr

def test_auto_corr():
    # Create an instance of AutoCorr
    auto_corr = AutoCorr()

    # Optionally, generate test data (if method is available)
    auto_corr.GenerateTestData()

    # Test adding a new autocorrection item
    auto_corr.InsertItem("test", "TEST")
    
    # Test replacing an existing item
    # You need to know the index of the item you want to replace
    # This example assumes index 0
    auto_corr.ReplaceItem(0, "replace", "REPLACE")

    # Test deleting an item
    # This example assumes deleting the item at index 0
    auto_corr.DeleteItem(0)

    # Print the list to verify changes
    print("AutoCorr List:")
    auto_corr.PrintList()

    # Test finding and replacing a string
    sample_str = "This is a test string with alpha and beta."
    replaced_str = auto_corr.FindReplace(sample_str)
    print("Original String: ", sample_str)
    print("Replaced String: ", replaced_str)

# Execute the test function
if __name__ == "__main__":
    test_auto_corr()

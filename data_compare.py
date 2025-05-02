import pandas as pd
import cv2
import matplotlib.pyplot as plt

def align_data(data, timecol="time", scale=1.0, shift=0.0, invert=False):
    """Align data using the inputs from the user, this allows the user to manipulate the data without editing the file

    Args:
        data (pd.DataFrame): this is the input dataframe to align with the other one
        timecol (str, optional): name of the time column in the file. Defaults to "time".
        scale (float, optional): scaling multiplier. Defaults to 1.0.
        shift (float, optional): shifting factor. Defaults to 0.0.
        invert (bool, optional): whether to invert the data or not. Defaults to False.

    Returns:
        pd.DataFrame: this is the post-processed image
    """
    processed_data = data.copy()
    
    for col in processed_data.columns:
        if col != timecol:
            if invert:
                processed_data[col] *= -1
            processed_data[col] = processed_data[col] * scale + shift
            
    return processed_data
    
    
# change the value in "timecol" to be whatever the actual value is in the file
def load_csvs(file1_path, file2_path, timecol='time', scale1=1.0, shift1=0.0, invert1=False):
    """loads the csvs and turns them into pd.DataFrames

    Args:
        file1_path (string): directory to the first CSV file
        file2_path (string): directory to the second CSV file
        timecol (str, optional): name of the time column in both files. Defaults to 'time'.
        scale1 (float, optional): scaling factor to apply to file 1. Defaults to 1.0.
        shift1 (float, optional): shifting factor to apply to file 1. Defaults to 0.0.
        invert1 (bool, optional): whether or not to invert the axis in file 1. Defaults to False.

    Raises:
        ValueError: if there is no time column in the CSV files

    Returns:
        pd.DataFrame: this is the merged dataframe from both CSV files
    """
    
    # read in files
    f1 = pd.read_csv(file1_path)
    f2 = pd.read_csv(file2_path)
    
    # raise error if time column isn't found
    if timecol not in f1.columns or timecol not in f2.columns:
        raise ValueError(f"Time column '{timecol}' not found in both CSV files")
    
    f1_processed = align_data(f1, timecol, scale1, shift1, invert1)
    
    # merge files
    merge_files = pd.merge_asof(f1_processed.sort_values(timecol), f2.sort_values(timecol), on=timecol, direction='nearest')
    
    return f1_processed, f2, merge_files
        
def stacked_plots(file, timecol="time", title_suffix=""):
    """Creates a stacked plot figure of the input file

    Args:
        file (pd.DataFrame): input file to create a figure from
        timecol (str, optional): name of the time column. Defaults to "time".
        title_suffix (str, optional): the suffix to add to the title to differentiate files. Defaults to "".

    Returns:
        Figure : output figure from the file
    """
    # get columns and put them in data columns
    data_columns = [col for col in file.columns if col != timecol]
    
    # get the number of variables
    num_vars = len(data_columns)
    
    # create the figure (subplots is a cool functionality I've never used before)
    fig, axes = plt.subplots(num_vars, 1, figsize=(10, 2*num_vars), sharex=True)
    
    # unarray axes if there is only 1 variable
    if num_vars == 1:
        axes = [axes]
    
    # plot the variables
    for i, col in enumerate(data_columns):
        axes[i].plot(file[timecol], file[col], label=col)
        axes[i].set_ylabel(col)
        axes[i].grid(True)
        axes[i].legend()
    
    # set x label
    axes[-1].set_xlabel(timecol)
    
    # change the title for that plot
    plt.suptitle(f"Data from {title_suffix}")
    plt.tight_layout()
    return fig

def plot_to_image(fig, output_file):
    """Takes the stacked plot and turns it into a png image

    Args:
        fig (Figure): the input figure to turn into an image
        output_file (string): the name of the output image

    Raises:
        RuntimeError: This happens if the temporary file that is generated is none, this can occur if the input figure isn't generated or not generated correctly
    """
    
    # save figure to the temporary png
    temp_file = "temp_plot.png"
    fig.savefig(temp_file, dpi=300)
    plt.close(fig)
    
    # use cs2 to read the temp file then write it to the output file
    img = cv2.imread(temp_file)
    if img is not None:
        cv2.imwrite(output_file, img)
    else:
        raise RuntimeError("Failed to read temporary image file.")
    
    # I would import os here to delete the "temp_plot.png" file, but I technically am not allowed that import so I won't do that.
    print("Note: Temporary file 'temp_plot.png' was not automatically removed")
    
def main(file1, file2, output_prefix="stacked_plots", timecol="time", scale1=1.0, shift1=0.0, invert1=False):
    """Takes the input file directories and generates the image that is the figures

    Args:
        file1 (string): directory to CSV 1
        file2 (string): directory to CSV 2
        output_prefix (str, optional): prefix for the output images. Defaults to "stacked_plots".
        timecol (str, optional): name of the time column in the CSV files. Defaults to "time".
        scale1 (float, optional): scaling factor to apply to file 1. Defaults to 1.0.
        shift1 (float, optional): shifting factor to apply to file 1. Defaults to 0.0.
        invert1 (bool, optional): whether or not to invert the data columns in file 1. Defaults to False.
    """
    
    f1_processed, f2, merge_data = load_csvs(file1, file2, timecol, scale1, shift1, invert1)
    
    fig1 = stacked_plots(f1_processed, timecol, "File 1 (Processed)")
    plot_to_image(fig1, f"{output_prefix}_file1.png")
    
    fig2 = stacked_plots(f2, timecol, "File 2")
    plot_to_image(fig2, f"{output_prefix}_file2.png")
    
    fig_merged = stacked_plots(merge_data, timecol, "Merged Data")
    plot_to_image(fig_merged, f"{output_prefix}_merged.png")
    
    print(f"Plots saved to {output_prefix}_file1.png, {output_prefix}_file2.png, and {output_prefix}_merged.png")
    
# this next part is to make this work as a standalone script, but it could also work if you copy pasted the above lines into a jupyter notebook or another python file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv)<3:
        print("Usage python DataImport.py <file1.csv> <file2.csv> [output_prefix] [time_column_name] [scale1 (float)] [shift1 (float)] [invert1 (true or false)]")
        print("Example: python DataImport.py data1.csv data2.csv output timestamp 1.0 0.0 False")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_prefix = sys.argv[3] if len(sys.argv) > 3 else "stacked_plots"
    timecol = sys.argv[4] if len(sys.argv) > 4 else "time"
    scale1 = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    shift1 = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
    invert1 = sys.argv[7].lower() == 'true' if len(sys.argv) > 7 else False
    
    main(file1, file2, output_prefix, timecol, scale1, shift1, invert1)
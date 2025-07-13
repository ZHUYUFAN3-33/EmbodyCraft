import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from scipy.ndimage import gaussian_filter1d
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.renderers.default = 'browser'


def process_and_plot_v3(file_path, sampling_rate, num_channels, gauss_sigma):
    try:
        # Load CSV
        df = pd.read_csv(file_path, delimiter=',')

        # Detect timestamp column (case insensitive)
        if 'timestamp' in df.columns:
            time_col = 'timestamp'
        elif 'Timestamp' in df.columns:
            time_col = 'Timestamp'
        else:
            raise ValueError("CSV must contain a 'timestamp' column")

        df[time_col] = pd.to_datetime(df[time_col])
        df[time_col] = (df[time_col] - df[time_col].iloc[0]).dt.total_seconds()
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)

        # Interpolation and resampling
        target_interval = 1 / sampling_rate
        new_timestamps = np.arange(df[time_col].iloc[0], df[time_col].iloc[-1] + target_interval, target_interval)
        interpolated_data = pd.DataFrame({time_col: new_timestamps})
        for col in df.columns[1:num_channels + 1]:
            interpolated_data[col] = np.interp(new_timestamps, df[time_col], df[col])

        # Baseline correction
        calibrated_data = interpolated_data.copy()
        N = 45
        for col in calibrated_data.columns[1:]:
            baseline = np.mean(calibrated_data[col].head(N))
            calibrated_data[col] = calibrated_data[col] - baseline
            calibrated_data[col] = calibrated_data[col].clip(lower=0)

        # Normalize per channel
        normalized_data = calibrated_data.copy()
        for col in normalized_data.columns[1:]:
            scaler = MinMaxScaler()
            normalized_data[col] = scaler.fit_transform(normalized_data[[col]])

        # Gaussian filter per channel
        smoothed_data = normalized_data.copy()
        for col in smoothed_data.columns[1:]:
            smoothed_data[col] = gaussian_filter1d(smoothed_data[col], sigma=gauss_sigma)

        # Plot
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Before Gaussian Filter", "After Gaussian Filter"))
        for i in range(1, normalized_data.shape[1]):
            fig.add_trace(go.Scatter(x=normalized_data.iloc[:, 0],
                                     y=normalized_data.iloc[:, i],
                                     mode='lines',
                                     name=f'Ch{i} Norm'),
                          row=1, col=1)
            fig.add_trace(go.Scatter(x=smoothed_data.iloc[:, 0],
                                     y=smoothed_data.iloc[:, i],
                                     mode='lines',
                                     name=f'Ch{i} Smooth'),
                          row=1, col=2)

        fig.update_layout(
            title='FMG Signal Comparison: Normalized vs Smoothed',
            width=1800,
            height=600,
            template='plotly_white',
            showlegend=False
        )
        fig.update_xaxes(title_text='Time (s)', row=1, col=1)
        fig.update_xaxes(title_text='Time (s)', row=1, col=2)
        fig.update_yaxes(title_text='Value', row=1, col=1)
        fig.update_yaxes(title_text='Value', row=1, col=2)
        fig.show()

        # Save
        save_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV files", "*.csv")],
            title="Save processed data"
        )
        if save_path:
            smoothed_data.to_csv(save_path, header=True, index=False)

    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"Failed to process file:\n{e}")


def launch_gui():
    root = tk.Tk()
    root.title("FMG Gaussian Filter Tool")
    root.geometry("400x200")

    def start_processing():
        file_path = filedialog.askopenfilename(
            title="Select FMG CSV file",
            filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            return

        try:
            sampling_rate = simpledialog.askinteger("Sampling Rate", "Enter target sampling rate (e.g., 30):")
            if sampling_rate is None or sampling_rate <= 0:
                raise ValueError("Invalid sampling rate.")

            num_channels = simpledialog.askinteger("Channel Count", "Enter number of channels (e.g., 8):")
            if num_channels is None or num_channels <= 0:
                raise ValueError("Invalid channel count.")

            gauss_sigma = simpledialog.askfloat("Gaussian Sigma", "Enter Gaussian filter sigma (e.g., 2.0):")
            if gauss_sigma is None or gauss_sigma <= 0:
                raise ValueError("Invalid sigma.")

            process_and_plot_v3(file_path, sampling_rate, num_channels, gauss_sigma)

        except Exception as e:
            messagebox.showerror("Input Error", str(e))

    tk.Label(root, text="FMG Gaussian Filter Processor", font=('Arial', 14)).pack(pady=10)
    tk.Button(root, text="Select File and Start", command=start_processing).pack(pady=20)
    root.mainloop()


if __name__ == '__main__':
    print("Launching GUI...")
    launch_gui()

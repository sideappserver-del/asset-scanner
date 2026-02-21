import tkinter as tk

# Create window
window = tk.Tk()
window.title('?? Asset Scanner - Test')
window.geometry('400x200')

# Add label
label = tk.Label(window, text='If you see this, Python is working! ?', font=('Arial', 12))
label.pack(pady=20)

# Add button
button = tk.Button(window, text='Close', command=window.quit)
button.pack()

# Run
window.mainloop()
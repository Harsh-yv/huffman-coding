import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
def compress(file_path):
    ascii_frequencies = calculate_ascii_frequencies(file_path)
    values=list(ascii_frequencies.keys())
    freqs=list(ascii_frequencies.values())
    freqs,values=heapify(len(freqs),freqs,values)
    a=list(freqs)
    code=[]
    for i in values:
        code+=[[[i,""]]]
    print(a)
    print(code)
    while(len(a)>1):
        b=a.pop(0)
        c=code.pop(0)
        for i in c:
            i[1]="0"+i[1]
        a,code=heapify(len(a),a,code)
        b=b+a.pop(0)
        a+=[b]
        for i in code[0]:
            i[1]="1"+i[1]
        code[0]=c+code[0] 
        freqs.append(a[0])
        a[0],a[len(a)-1]=a[len(a)-1],a[0]
        a,code=heapify(len(a),a,code)
    if ascii_frequencies is not None:
        print("ASCII Frequencies:")
        for ascii_value,freq in ascii_frequencies.items():
            print(f"ASCII {chr(ascii_value)},{freq}")
        
    for i in range(len(values)):
        m=values[i]
        n=freqs[i]
        print(i,chr(m),n)  
    print(freqs)
    print(code)
    dic={}
    code_long=[]
    code_short=[]
    coded=""
    for i in code[0]:
        dic[i[0]]=i[1]
        code_long.append(i[0])
        code_short.append(i[1])
        coded+=str(i[0])+":"+i[1]+" "
    print(coded)
    mssg=""
    try:
        with open(file_path, 'r') as file:
            for char in file.read():
                mssg+=dic[ord(char)]           
    except FileNotFoundError:
        print(f"decompoError: The file {file_path} does not exist.")
    print(mssg)
    coded_txt="Code:"+coded+"Message:"+mssg
    print(coded_txt)
    return coded_txt

def decompress(file_path):
    coded_txt=""
    try:
        with open(file_path, 'r') as file:
            for char in file.read():
                coded_txt+=char
    except FileNotFoundError:
        print(f"decompoError: The file {file_path} does not exist.")
    print("wow"+coded_txt)
    coder=coded_txt.lstrip("Code:")
    print(coder)
    code_list=coder.split(" Message:")
    print(code_list)
    dicto={}
    code_long=[]
    code_short=[]
    for i in code_list[0].split():
        j=i.split(":")
        dicto[int(j[0])]=j[1]
        code_long.append(int(j[0]))
        code_short.append(j[1])
    print(dicto)
    decoded=""
    left=""
    for i in code_list[1]:
        left+=i
        if left in code_short:
            decoded+=chr(code_long[code_short.index(left)])
            left=""
    print(decoded)
    return decoded
def calculate_ascii_frequencies(file_path):
    ascii_freq = {}
    try:
        with open(file_path, 'r') as file:
            for char in file.read():
                ascii_value = ord(char)
                if(ascii_value not in ascii_freq):
                    ascii_freq[ascii_value]=0
                ascii_freq[ascii_value] += 1
        return ascii_freq     
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
def heapify(max,freqs,code):
    for i in range(max//2-1,-1,-1):
        largest=i
        l = 2 * i + 1
        r = 2 * i + 2
        if (l < max and freqs[l] < freqs[largest]):
            largest = l
        if (r < max and freqs[r] < freqs[largest]):
            largest = r
        if (largest != i) :
            freqs[i],freqs[largest]=freqs[largest],freqs[i]
            code[i],code[largest]=code[largest],code[i]
    return freqs,code
def compress_file():
    """Open a text file, copy its contents to another file."""
    file_path = filedialog.askopenfilename(title="Open Text File", filetypes=[("Text Files", "*.txt")])
    
    if file_path:
        try:
            coded_txt=compress(file_path)
            save_path = filedialog.asksaveasfilename(title="Save As", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if save_path:
                with open(save_path, 'w') as new_file:
                    new_file.write(coded_txt)
                messagebox.showinfo("Success", "File content compressed successfully!")
            else:
                messagebox.showwarning("No Save Location", "No location selected to save the compressed file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("No File Selected", "No file selected to open.")
def decompress_file():
    """Open a text file, copy its contents to another file."""
    file_path = filedialog.askopenfilename(title="Open Text File", filetypes=[("Text Files", "*.txt")])
    
    if file_path:
        try:
            decoded_txt=decompress(file_path)
            
            save_path = filedialog.asksaveasfilename(title="Save As", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            
            if save_path:
                with open(save_path, 'w') as new_file:
                    new_file.write(decoded_txt)
                messagebox.showinfo("Success", "File content decompressed successfully!")
            else:
                messagebox.showwarning("No Save Location", "No location selected to save the decompressed file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("No File Selected", "No file selected to open.")
def create_app():
    """Create the GUI for the app."""
    root = tk.Tk()
    root.title("File Operations App")
    root.geometry("300x200")
    
    copy_button = tk.Button(root, text="Compress File", command=compress_file)
    copy_button.pack(pady=20)
    
    count_button = tk.Button(root, text="Decompress File", command=decompress_file)
    count_button.pack(pady=20)
    
    root.mainloop()
if __name__ == "__main__":
    create_app()

#!/usr/bin/env python3
import tkinter as tk
from AddComment import AddAnnotation
import tempfile
from tkinter import filedialog
import tkinter.font as tkFont
import os,json
from tkinter import messagebox
def select_pdf():
    # 通过文件选择框来选择PDF文件
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_input.delete(0, tk.END)
        pdf_input.insert(0, file_path)
        pdf_input.config(fg='black', width=15)
    else:
        pdf_input.config(fg='black', width=0)
    check_run_button()
config_path = ""
input_pdf = ""
def select_config():
    # 通过文件选择框来选择配置文件
    global config_path
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.json")])
    config_path = file_path
    config_text.delete("1.0", tk.END)
    with open(file_path, "r") as f:
        content = f.read()
    try:
        json_content = json.loads(content)
        formatted_content = json.dumps(json_content, indent=8)

        config_text.delete(1.0, tk.END)
        # config_text.insert("1.0", formatted_content)
        config_text.tag_configure('html', font=('Arial', 10), foreground='black')
        config_text.insert(tk.END, formatted_content, 'html')
        check_run_button()

    except:
        messagebox.showerror("Error", "Error loading JSON content from selected file!")




def check_run_button():
    # 检查是否可以启用Run按钮
    print( pdf_input.get()  )
    if pdf_input.get() and config_text.get("1.0", tk.END):
        run_button.config(state="normal")
    else:
        run_button.config(state="disabled")

def run_analysis():
    # 进行注释分析，并将结果保存到文件中
    pdf_file = pdf_input.get()
    config_file = config_text.get("1.0", tk.END)
    # TODO: 进行注释分析
    result_file = tempfile.mktemp()[1]
    LOG = open( "log.log",'w' )
    with open("log.log", "w") as LOG:
        LOG.write("PDF 文件：{}\n配置文件：{}".format(pdf_file, config_file))
    print( config_path)
    # AddAnnotation(pdf_file,)
    # download_result(result_file,result_file)

def download_result(result_file):
    save_path = filedialog.asksaveasfilename(title="保存结果", initialfile="Output.pdf", filetypes=[('Text Files', '*.txt')])
    if save_path:
        with open(result_file, 'r') as f:
            content = f.read()
        with open(save_path, 'w') as f:
            f.write(content)
        os.remove(result_file)
# 创建主窗口
root = tk.Tk()
root.title("AnnotationAnalysis")
font = tkFont.Font(family="黑体", size=14, weight="bold")
# 创建第一个区域：PDF输入
pdf_frame = tk.Frame(root, height=100)
pdf_frame.pack(fill="x", padx=20, pady=(100, 20))
pdf_label = tk.Label(pdf_frame, text="PDF 输入:",font=font,)
pdf_label.pack(side="top")

pdf_button = tk.Button(pdf_frame, text="选择文件", width=15, command=select_pdf)
pdf_input = tk.Entry(pdf_frame,   highlightthickness=0 ,bd=0, width=0 ,highlightbackground="gray")


pdf_input.pack(side="top", padx=0, expand=True)
pdf_button.pack(side="top", padx=10)



# 创建分割线
sep1 = tk.Canvas(root, height=2, bg="black", highlightthickness=0, bd=0, relief='ridge', highlightcolor="gray",
              highlightbackground="gray", )
sep1.pack(fill="x", padx=20, pady=20, anchor="n")

# 创建第二个区域：配置文件输入
config_frame = tk.Frame(root, height=400)
config_frame.pack(fill="x", padx=20, pady=20)
config_label = tk.Label(config_frame, text="配置文件输入:",font=font)
config_label.pack(side="top")
config_upload = tk.Button(config_frame, text="上传文件", width=15, command=select_config)
config_upload.pack(side="top", pady=10)
config_text = tk.Text(config_frame, height=10)
config_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a Scrollbar widget
scrollbar = tk.Scrollbar(config_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the Scrollbar to the Text widget
config_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=config_text.yview)

# 创建分割线
sep2 = tk.Canvas(root, height=2, bg="black", highlightthickness=0, bd=0, relief='ridge', highlightcolor="gray",
              highlightbackground="gray", )
sep2.pack(fill="x", padx=20, pady=20, anchor="n")

# 创建第三个区域：运行按钮
run_frame = tk.Frame(root, height=50,)
run_frame.pack(fill="x", padx=20, pady=20)

run_button = tk.Button(run_frame, text="Run",font=font, width=10, height=2, command=run_analysis, state="disabled")
run_button.pack(pady=10)

# 检查Run按钮是否可用
check_run_button()

# 运行主循环
root.mainloop()


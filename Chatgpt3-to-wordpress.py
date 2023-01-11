import tkinter as tk
from tkinter import filedialog
import os
from tkinter import messagebox
import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost


def generate_text():
    # Get the prompt from the user
    prompt = input_field.get()

    openai.api_key = "input API key here"

    # Call the GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3500
    )

    # Print the generated text
    output_field.delete(1.0, tk.END)
    output_field.insert(tk.END, response["choices"][0]["text"])


def save_text():
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if os.path.exists(save_path):
        messagebox.showwarning("Save Text", "File already exists, do you want to overwrite it?", parent=root)
        if messagebox.askyesno("Save Text", "Are you sure you want to overwrite the file?", parent=root):
            with open(save_path, "w") as f:
                f.write(output_field.get(1.0, tk.END))
        else:
            messagebox.showinfo("Save Text", "The file was not overwritten", parent=root)
    else:
        with open(save_path, "w") as f:
            f.write(output_field.get(1.0, tk.END))


def post_to_wordpress():
    wp = Client('https://your-wordpress-site.com/xmlrpc.php', 'your_username', 'your_password')
    post = WordPressPost()
    post.title = 'GPT-3 integration with WordPress'
    post.content = output_field.get(1.0, tk.END)
    post.terms_names = {
        'post_tag': ['gpt-3', 'wordpress'], 'category': ['Tutorial']
    }
    post.post_status = 'publish'
    wp.call(NewPost(post))


def paraphrase_text():
    save_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    with open(save_path, "r") as f:
        text_to_paraphrase = f.read()
    prompt = f"paraphrase following text: {text_to_paraphrase}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3500
    )
    paraphrased_text = response["choices"][0]["text"]
    output_field.delete(1.0, tk.END)
    output_field.insert(tk.END, paraphrased_text)

# Create a new Tkinter window
root = tk.Tk()
root.title("GPT-3 Article Generator")

# Create a label for the input field
input_label = tk.Label(root, text="Enter your prompt:")
input_label.grid(row=0, column=0)

# Create a text field for the input
input_field = tk.Entry(root)
input_field.grid(row=0, column=1)

# Create a button to generate the text
generate_button = tk.Button(root, text="Generate Text", command=generate_text)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

# Create a text field for the output
output_field = tk.Text(root)
output_field.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Create a button to save the text
save_button = tk.Button(root, text="Save Text", command=save_text)
save_button.grid(row=3, column=0, padx=10)

# Create a button to post the text to WordPress
post_button = tk.Button(root, text="Post to WordPress", command=post_to_wordpress)
post_button.grid(row=3, column=1, padx=10)

# Create a button to paraphrase the text
paraphrase_button = tk.Button(root, text="Paraphrase Text", command=paraphrase_text)
paraphrase_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

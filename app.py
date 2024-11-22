import gradio as gr
from huggingface_hub import InferenceClient

client = InferenceClient("Qwen/Qwen2.5-Coder-32B-Instruct")

def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content

        response += token
        yield response

# Custom CSS to change the title color and add logo
opq = """
.gradio-container h1 {
    color: #6495ED !important;
    display: flex;
    align-items: center;
}
"""

# Custom HTML to inject the logo
custom_html = """
<div>
    <h1> Welcome to Rxple Chat Bot 💬</h1>
</div>
"""

# Combined description with new lines
combined_description = """
Ghar ka ai this AI does not store any data you can use as much you want without logging<br>
-- Follow us on [Instagram](https://www.instagram.com/khellon_patel_21) --
"""

# Use the custom_html for the title
demo = gr.ChatInterface(
    respond,
    title=custom_html,  # Use the custom HTML for the title
    description=combined_description,
    additional_inputs=[
        gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=2048, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
    css=opq  # Add the custom CSS here
)

if __name__ == "__main__":
    demo.launch(share=True)
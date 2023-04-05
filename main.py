import openai
import gradio as gr

openai.api_key = open("key.txt", "r").read().strip()
message_history = [{"role": "user", "content": f"You are a joke bot. I will specify the subject matter in my messages, and you will reply with a joke that includes the subjects I mention in my messages. Reply only with jokes to further input. If you understand, say OK."},
                   {"role": "assistant", "content": f"OK"}]


def predict(input):
    global message_history
    message_history.append({"role":"user", "content":input})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )

    response_content = completion.choices[0].message.content
    message_history.append({"role":"assistant", "content":response_content})
    print(response_content)
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in range(2, len(message_history) - 1, 2)]
    return response
    # return response_content

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        text = gr.Textbox(show_label=False, placeholder="Type your message here").style(container=False)
        text.submit(predict, text, chatbot)
        text.submit(lambda: "", None, text)
        # text.submit(None, None, text, _js="() => {''}")
    demo.launch()

# demo = gr.Interface(fn=predict, inputs="text", outputs="text")
# demo.launch()

import gradio as gr
from allergene import chatbot_pizza_allergens


def respond_to_user(message, history):
    """
    Fonction qui gère les réponses du chatbot
    """
    if not message:
        return "", history

    response = chatbot_pizza_allergens(message)

    history.append((message, response))

    return "", history


def create_interface():
    """
    Crée l'interface Gradio pour le chatbot
    """
    with gr.Blocks(title="Chatbot Pizza") as interface:
        gr.Markdown(
            """
            # Chatbot Pizza
            
            Posez vos questions sur les allergènes présents dans les pizzas.
            
            **Important**: Recommandation de toujours vérifier avec le restaurant en cas d'allergie grave.
            """
        )

        chatbot = gr.Chatbot(label="Discussion", height=200, bubble_full_width=False)

        msg = gr.Textbox(
            label="Votre question",
            placeholder="Ex: Quels sont les allergènes dans la pizza Margherita ?",
            lines=2,
        )

        with gr.Row():
            submit = gr.Button("Envoyer", variant="primary")
            clear = gr.Button("Effacer")
        gr.Examples(
            examples=[
                "Quels sont les allergènes dans la pizza Margherita ?",
                "Est-ce que la pizza 4 fromages contient du gluten ?",
                "Y a-t-il des pizzas sans lactose ?",
                "Quelles pizzas contiennent des fruits de mer ?",
                "La pizza végétarienne contient-elle des noix ?",
            ],
            inputs=msg,
        )

        msg.submit(respond_to_user, [msg, chatbot], [msg, chatbot])
        submit.click(respond_to_user, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: (None, []), None, [msg, chatbot])

    return interface


if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        server_name="127.0.0.1", server_port=7860, share=False, inbrowser=True
    )

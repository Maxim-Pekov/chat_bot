import os

import requests
from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main() -> None:
    """Start the bot."""
    load_dotenv()

    project_id = os.getenv('PROJECT_ID')
    url = 'https://dvmn.org/media/filer_public/a7/db/' \
          'a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'

    response = requests.get(url)
    response.raise_for_status()
    intents = response.json()

    for intent, values in intents.items():
        training_phrases_parts = values['questions']
        message_text = values['answer']
        message_texts = [message_text]

        create_intent(
            project_id, intent, training_phrases_parts, message_texts
        )


if __name__ == '__main__':
    main()
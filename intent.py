import os

import requests
from dotenv import load_dotenv
from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text,
                                          language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        response_text = response.query_result.fulfillment_text
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        return response_text


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
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
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
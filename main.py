from google import genai
from google.genai import types
import uuid
import time
import pathlib

GOOGLE_GEMINI_API_KEY = ""  # Replace with your actual API key from https://aistudio.google.com/app/apikey?hl=he
client = genai.Client(api_key=GOOGLE_GEMINI_API_KEY)
model = "gemini-2.0-flash-thinking-exp-01-21" # Uses Gemini 2.0 Flash "thinking" experimental model, can be changed, exp-01-21 might not be available anymore as it is not a finalized version.
model2 = "gemini-2.0-flash" # Uses the finalized version of the Gemini 2.0 Flash model.
filepath = pathlib.Path("testcontract1.pdf")

# Function takes the prompt, runs it through the refinement process using the feedback, and returns the refined prompt.

def call_gemini_api_refiner(prompt,feedback):

    input_data = ("please make this prompt better, in your answer, only inlcude the new and improved prompt, no extra chatter, do not attempt to include other data structures such as JSON to the prompt's working, the prompts should output textual data that is easy to read, the prompt should understand those details from the file and be able to outline them, it should not copy entire sentences, but rather put them in an easier to understand format, do not simplify the prompt, make sure it stays on the topic of extracting information from the contract: ") + prompt+"\n\nalso, make sure to include the following advice in your response: "+feedback

    refined_prompt = client.models.generate_content(model=model,contents=input_data)

    return refined_prompt

# Function takes the prompt, tests it on the sample contract, and then provides advice for futher refinement.

def call_gemini_api_feedback(prompt):

    input_data = ("Using this prompt and the attached file, please include your feedback and points for improvement, what points did it miss? what should it watch out for?, only include your suggestions in the result, do not include any chatter, do not add advice to simplify the prompt, use other data structures, and keep your advice limited to better data extraction, do not include any actual details from the document, limit your response to 50 words\n\n") + prompt

    feedback = client.models.generate_content(
        model=model2,
        contents=[
            types.Part.from_bytes(
            data=filepath.read_bytes(),
            mime_type="application/pdf",
        ),
        input_data])

    return feedback.text



if __name__ == "__main__":
    file_id = uuid.uuid4() # Using the UUID module to generate a unique file name to avoid conflict between runs.
    file_name= "juror/"+str(file_id) + ".txt" # Files will be stored in a different folder to avoid clutter.
    file = open(file_name, "w")
    prompt = input("Enter the prompt (or 'exit' to quit): ") # Takes the generic prompt that the user wants to refine.
    n = input("Enter the number of iterations: ") # Takes the number of iterations the user wants to run the prompt through.
    counter = 0
    feedback = ''
    if prompt == "exit":
        exit()
    for i in range(1,int(n)+1):
        file.write(prompt + "\n" + "----ADVICE----\n" + feedback + "\n" + str(counter) + "\n") # Writes the current, pre-refined prompt to the file along with its iteration number and the future advice for it.
        print(counter) # Debug prints the iteration counter so we can see how far the process has gone.

        refined_prompt = call_gemini_api_refiner(prompt,feedback) # Calls the function to refine the prompt using the feedback, first iteration will have no feedback.
        prompt = refined_prompt.text # Updates the prompt variable with the refined prompt.

        time.sleep(5) # To avoid rate limiting
        feedback = call_gemini_api_feedback(prompt) # Generates future advice based on the refined prompt
        counter += 1 # Increments the counter.
        time.sleep(5) # To avoid rate limiting
    file.close() # At the end of the process, the file is closed to avoid data loss.


import google.generativeai as gemini
import uuid
import time

GOOGLE_GEMINI_API_KEY = ""  # Replace with your actual API key from https://aistudio.google.com/app/apikey?hl=he
gemini.configure(api_key=GOOGLE_GEMINI_API_KEY)
model = gemini.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21") # Uses Gemini 2.0 Flash "thinking" experimental model, can be changed, exp-01-21 might not be available anymore as it is not a finalized version.

# Function takes the prompt, runs it through the refinement process, and returns the refined prompt.
def call_gemini_api(prompt):

    input_data = ("please make this prompt better, in your answer, only inlcude the new and improved prompt, no extra chatter, do not attempt to include other data structures such as JSON to the prompt's working, the prompts should output textual data that is easy to read, the prompt should understand those details from the file and be able to outline them, it should not copy entire sentences, but rather put them in an easier to understand format, do not simplify the prompt, make sure it stays on the topic of extracting information from the contract. ") + prompt

    refined_prompt = model.generate_content(input_data)

    return refined_prompt


if __name__ == "__main__":
    file_id = uuid.uuid4() # Using the UUID module to generate a unique file name to avoid conflict between runs.
    file_name= "juror/"+str(file_id) + ".txt" # Files will be stored in a different folder to avoid clutter.
    file = open(file_name, "w")
    prompt = input("Enter the prompt (or 'exit' to quit): ") # Takes the generic prompt that the user wants to refine.
    n = input("Enter the number of iterations: ") # Takes the number of iterations the user wants to run the prompt through.
    counter = 0
    if prompt == "exit":
        exit()
    for i in range(1,int(n)+1):
        file.write(prompt +  "\n" + str(counter) + "\n") # Writes the current, pre-refined prompt to the file along with its iteration number.
        print(counter) # Debug prints the iteration counter so we can see how far the process has gone.
        refined_prompt = call_gemini_api(prompt) # Calls the function to refine the prompt.
        prompt = refined_prompt.text # Updates the prompt variable with the refined prompt.
        counter += 1 # Increments the counter.
        time.sleep(5) # Sleeps for 5 seconds to avoid rate limiting.
    file.close() # At the end of the process, the file is closed to avoid data loss.


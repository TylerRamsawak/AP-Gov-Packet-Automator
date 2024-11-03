import os
import google.generativeai as genai

genai.configure(api_key="")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-002",
  generation_config=generation_config,
  system_instruction="Fill out the given topic with details related to AP Government. Be cool, be simple, "
                     "and straight to the point. Do NOT be repetitive. Do not double space.",
)

chat_session = model.start_chat(
  history=[
  ]
)


def decode_unit():
    prompt_line_number = []
    prompt_count = 0
    with open('Reading Guide - Unit 2 - Part 2.txt', 'r') as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if line != '\n':
                prompt_count += 1
                prompt_index = i
                prompt_line_number.append(prompt_index)

        # print(prompt_line_number)

        lines_between_prompt = []
        for i in range(1, len(prompt_line_number)):
            lines_between_prompt.append((prompt_line_number[i]-prompt_line_number[i-1])-1)
        lines_between_prompt.append(10) # im appending this number to simulate the last space below the last prompt.
        # since there is no last_prompt+1, because it does not exist, we cannot find the difference.
        # so, just add an imaginary space that we assume to be 10.

        # print(lines_between_prompt)

        page_width = 216 #mm
        margin = 24 #mm
        line_h = 2.5 #mm
        char_w = 2.5 #mm
        char_h = 3 #mm
        usable_width = page_width-(margin*2)
        usable_chars = []
        for i in range(0, len(lines_between_prompt)):
            usable_chars.append(((lines_between_prompt[i] * line_h) // char_h) * (usable_width // char_w))

        # print(usable_chars)

        prompts_pretty = {}
        for i in range(0, len(prompt_line_number)):
            temp = {"line": prompt_line_number[i], "prompt": lines[prompt_line_number[i]][:-1],
                    "new_lines": lines_between_prompt[i], "chars": usable_chars[i]}
            prompts_pretty[i] = temp
            # print(f'At line {prompt_line_number[i]}, the prompt is {lines[prompt_line_number[i]]}There are {
            # lines_between_prompt[i]} lines below it, making for a total of {usable_chars[i]} characters available\n')

        print(prompts_pretty)
        return prompts_pretty


def AI_fetch(prompts, f):
    responses = []
    for i in range(f, len(prompts)):
        if i < f+15: # limit
            prompt = prompts[i]["prompt"]
            chars = prompts[i]["chars"]
            response = chat_session.send_message(f'In less than {chars} characters, fill out: {prompt}')
            print(response.text)
            responses.append(response.text)

    print(responses)
    return responses


def to_paper(responses):
    test=1


if __name__ == '__main__':
    from_paper = decode_unit()
    start = 16
    gemini_responses = AI_fetch(from_paper, start)
    #to_paper(gemini_responses)

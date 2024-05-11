from flask import Flask, render_template, request
import openai
import random

app = Flask(__name__)

openai.api_key = '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'

def generate_start(preferences):
    prompt = ""
    if preferences['genre'] == 'story':
        prompt += f"Generate a fictional story in the genre {preferences['genres']} and in the language {preferences['language']}. The backdrop and setting of the story throughout should be - {preferences['setting']} and have a {preferences['mood']} mood."
    elif preferences['genre'] == 'script':
        prompt += f"Generate a professional movie script. The backdrop and setting of the script should be - {preferences['setting']} and have a {preferences['mood']} mood."
        prompt += f"It should be in the language {preferences['language']}."

    if preferences['genre'] == 'story':
        prompt += f" The main character is {preferences['protagonist']}."
        if preferences['protagonist_background_choice'] == 'Yes':
            prompt += f" The main character has a backstory: {preferences['protagonist_background']}."

    if preferences['genre'] == 'script':
        prompt += f" The protagonist is {preferences['protagonist']}."
        if preferences['protagonist_background_choice'] == 'Yes':
            prompt += f" The main character has a backstory: {preferences['protagonist_background']}."

    prompt += f" Remember that the whole {preferences['genre']} should follow {preferences['storyline']} as a guide, but take freedom to create and make the content interesting."
    return openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1500
    ).choices[0].text.strip()

def generate_middle(preferences, start):
    prompt = ""
    if preferences['genre'] == 'story':
        prompt = f"Generate a seamless and with good transition which is in the genre {preferences['genres']}- a middle part of the story that builds on the start: {start}."
        prompt += f"It should be in the language {preferences['language']}."
    elif preferences['genre'] == 'script':
        prompt = f"Generate a seamless and with good transition which is in the genre {preferences['genres']}- a middle part of the script that builds on the start: {start}."
        prompt += f"It should be in the language {preferences['language']}."

    if preferences['plot_twist_choice'] == 'Yes':
        prompt += f" Introduce an unexpected plot twist: {preferences['plot_twist_description']} such that the course of things should change."

    prompt += f" The main character encounters various challenges and meets new characters that cause trouble."

    if preferences['genre'] == 'story' and preferences['antagonist_choice'] == 'Yes':
        prompt += f" The protagonist comes face to face with the antagonist for the first time. The antagonist's name is {preferences['antagonist_name']}."

    if preferences['genre'] == 'script' and preferences['antagonist_choice'] == 'Yes':
        prompt += f" The antagonist has the following personality traits: {preferences['antagonist_personality_traits']} and background: {preferences['antagonist_background']}."

    prompt += f" Remember that the whole {preferences['genre']} should follow {preferences['storyline']} as a guide, but take freedom to create and make the content interesting."
    return openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1500
    ).choices[0].text.strip()

def generate_end(preferences, start, middle):
    prompt = ""
    if preferences['genre'] == 'story':
        prompt += f"This is the start of the story: {start}"
        prompt += f"It should be in the language {preferences['language']}."
        prompt += f" This is the middle of the story: {middle}"
        prompt += f" in the genre {preferences['genres']} Write a proper and interesting ending for the story that concludes the plot and gives a sense of closure."
    elif preferences['genre'] == 'script':
        prompt = f"This is the start of the script: {start}"
        prompt += f" This is the middle of the script: {middle}"
        prompt += f"in the genre {preferences['genres']} Write a proper and interesting ending for the script that brings the story to a climax and resolves the conflicts."

    prompt += f" Remember that the whole {preferences['genre']} should follow {preferences['storyline']} as a guide, but take freedom to create and make the content interesting."
    return openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1500
    ).choices[0].text.strip()

def generate_title(preferences, start, middle, end,comic):
    prompt = ""
    if preferences['genre'] == 'story':
        prompt = f"This is the start of the story: {start}"
        prompt += f"in the genre {preferences['genres']}"
        prompt += f" This is the middle of the story: {middle}"
        prompt += f" This is the end of the story: {end}"
        prompt += f" Generate an interesting and catchy title for the story."
    elif preferences['genre'] == 'script':
        prompt = f"This is the start of the script: {start}"
        prompt += f"in the genre {preferences['genres']}"
        prompt += f" This is the middle of the script: {middle}"
        prompt += f" This is the end of the script: {end}"
        prompt += f" Generate an interesting and catchy title for the script."
    elif preferences['genre'] == 'comic':
        prompt += f" This is the comic strip: {comic}"
        prompt += f"in the genre {preferences['genres']}"
        prompt += f" Generate an interesting and catchy title for the comic strip."

    return openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=200
    ).choices[0].text.strip()

def generate_dalle_image(prompt):
    try:
        if prompt:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
            )
            image_url = response["data"][0]["url"]
            return image_url
    except Exception as e:
        print(e)
        return "There was an issue in generating the image. Please try again later"

def generate_comic_strip(preferences):
    random_num = random.randint(11, 20)
    prompt = f"Generate a long comic strip in the genre {preferences['genres']} and in the language {preferences['language']}with proper start, middle and an end. The backdrop and setting of the story throughout should be - {preferences['setting']} and have a {preferences['mood']} mood."
    prompt += f" The main character is {preferences['protagonist']}."
    if preferences['protagonist_background_choice'] == 'Yes':
        prompt += f" The main character has a backstory: {preferences['protagonist_background']}."
    if preferences['plot_twist_choice'] == 'Yes':
        prompt += f" Introduce an unexpected plot twist: {preferences['plot_twist_description']} such that the course of things should change."
    if preferences['antagonist_choice'] == 'Yes':
        prompt += f" The antagonist has the following personality traits: {preferences['antagonist_personality_traits']} and background: {preferences['antagonist_background']}."
    prompt += f" Remember that the whole {preferences['genre']} should follow {preferences['storyline']} as a guide, but take freedom to create and make the content interesting."
    prompt += f" with {random_num} strips. and give the output with gaps between the each strip."
    return openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=3000
    ).choices[0].text.strip()

def image(preferences,title, start, middle,end,comic):
    if preferences['genre'] == 'story' or preferences['genre'] == 'script':
        prompt = f"For the given title of a story - {title}"
        prompt += f"\n\nThe start of the story is: {start}"
        prompt += f"\n\nThe middle of the story is: {middle}"
        prompt += f"\n\nThe end of the story is: {end}"
        prompt += f"\n\nFor this story and title, generate a prompt that can be used in DALL·E for comic strip generation."
    elif preferences['genre'] == 'comic':
        prompt = f"For the given title of a comic strip - {title}"
        prompt += f"\n\nThe comic strip is: {comic}"
        prompt += f"\n\nFor these title and comic strip, Generate a prompt that can be used in DALL·E for comic strip generation."
    if prompt:
        return openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=200
        ).choices[0].text.strip()

@app.route('/', methods=['GET', 'POST'])
def generate_story():
    if request.method == 'POST':
        try:
            genre = request.form['genre']
            genres = request.form['genres']
            language = request.form['language']
            setting = request.form['setting']
            protagonist = request.form['protagonist']
            mood = request.form['mood']
            plot_twist_choice = request.form['plot_twist_choice']
            plot_twist_description = ""
            if plot_twist_choice == 'Yes':
                plot_twist_description = request.form['plot_twist_description']
            protagonist_background_choice = request.form['protagonist_background_choice']
            protagonist_background = ""
            if protagonist_background_choice == 'Yes':
                protagonist_background = request.form['protagonist_background']
            antagonist_choice = request.form['antagonist_choice']
            antagonist_name = ""
            antagonist_personality_traits = ""
            antagonist_background = ""
            if antagonist_choice == 'Yes':
                antagonist_name = request.form['antagonist_name']
                antagonist_personality_traits = request.form['antagonist_personality_traits']
                antagonist_background = request.form['antagonist_background']
            storyline = request.form['storyline']

            preferences = {
                'genre': genre,
                'genres': genres,
                'setting': setting,
                'language': language,
                'protagonist': protagonist,
                'mood': mood,
                'plot_twist_choice': plot_twist_choice,
                'plot_twist_description': plot_twist_description,
                'protagonist_background_choice': protagonist_background_choice,
                'protagonist_background': protagonist_background,
                'antagonist_choice': antagonist_choice,
                'antagonist_name': antagonist_name,
                'antagonist_personality_traits': antagonist_personality_traits,
                'antagonist_background': antagonist_background,
                'storyline': storyline
            }

            comic_strip = None
            start = None
            middle = None
            end = None
            if genre == 'comic':
                comic_strip = generate_comic_strip(preferences)
            elif genre =='story' or genre =='script':
                start = generate_start(preferences)
                middle = generate_middle(preferences, start)
                end = generate_end(preferences, start, middle)
            title = generate_title(preferences, start, middle, end,comic_strip)
            image_prompt = image(preferences,title, start, middle, end,comic_strip)
            image_url = generate_dalle_image(image_prompt)

            return render_template('index.html', title=title, start=start, middle=middle, end=end, image_url=image_url, comic_strip=comic_strip, preferences=preferences)
        except Exception as e:
            error_message = "An error occurred while generating the story."
            print(e)
            return render_template('index.html', error_message=error_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
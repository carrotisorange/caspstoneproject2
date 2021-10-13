# import all the packages
from flask import Flask, render_template, request
from googletrans import Translator
import pandas as pd
import functions as function

translator = Translator()

app = Flask(__name__)


# 1. route for the search page
@app.route('/')
def search():
    return render_template('pages/index.html')


# 2. route for the screening
@app.route('/screen', methods=['POST'])
def screen():
    # 1. retrieve the input from the input field
    x = request.form['input']

    # 2. preprocess the input
    preprocessed_input = function.preprocess_input(x)

    # 3. validate the input
    validated_input = function.validate_input(preprocessed_input)

    if validated_input == 'rejectNumerical':
        return render_template('pages/index.html', error_message="Your input is not valid. Please enter a string.",
                               product_idea=validated_input)
    elif validated_input == 'rejectShortText':
        return render_template('pages/index.html', error_message="Your input is too short. Please enter a longer "
                                                                 "string.",
                               product_idea=validated_input)
    elif validated_input == 'languageNotSupported':
        return render_template('pages/index.html',
                               error_message="Your language is not supported. Please enter an English/Tagalog string "
                                             "only.", product_idea=validated_input)
    elif validated_input == 'inputIsNotANoun':
        return render_template('pages/index.html',
                               error_message="Your input is not a product idea. Please enter a noun."
                               , product_idea=validated_input)

    classified_input = function.classify_input(validated_input)

    return render_template("pages/screen.html", classification=classified_input, product_idea=validated_input)


# 3. routes for dashboard page
@app.route('/dashboard')
def dashboard():
    # datasets with complete complete product ideas
    product_ideas = pd.read_csv("C://Users//hp user//Desktop//MIT//caspstoneproject2//dataset//datasets.csv")
    product_ideas.dropna(subset=['product_idea'], inplace=True)

    # 5. get the top words based on frequency
    top_new_product_ideas = function.get_the_top_product_ideas(product_ideas.sort_values(by=['product_idea']))

    return render_template("pages/dashboard.html",
                           top_new_product_ideas=top_new_product_ideas.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

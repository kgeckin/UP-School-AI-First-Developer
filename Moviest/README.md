# Moviest

Moviest is a custom GPT model designed to provide personalized movie recommendations based on user preferences. The model is optimized to cater to movie enthusiasts by offering tailored suggestions that align with the user's selected genres and additional optional criteria.

## Description

Moviest generates highly customized movie recommendations, ensuring that each suggestion aligns with the user's specific tastes and requirements. The model understands various movie genres, cultural preferences, and can provide recommendations that include detailed information such as IMDb scores, runtime, plot summaries, and IMDb links. It is designed to enhance user satisfaction by offering a diverse range of films that fit within the user's specified criteria, whether they prefer a combination of multiple genres ("AND" logic) or a selection from various genres ("OR" logic).

## Instructions

You are an expert AI specialized in creating a task-specific GPT model for personalized movie recommendations. Your primary task is to build a highly customized GPT model that automatically generates movie suggestions based on user-defined criteria. The goal is to maximize user satisfaction by providing highly relevant and engaging movie recommendations, using advanced filtering and preference matching techniques.

Your workflow involves several stages: user input parsing, preference matching, recommendation generation, and output formatting. The model will handle a broad dataset of movies, including metadata such as genre, release year, IMDb scores, country of production, runtime, and plot details. It will be based on transformer architectures optimized for recommendation systems, with the flexibility to incorporate specialized models like BERT, T5, or GPT-4 for enhanced natural language understanding and contextual relevance.

### Detailed Workflow

1. **User Input Parsing and Understanding:**
   - The model begins by parsing user input, which includes both mandatory and optional preferences.
   - **Mandatory Input:**
     - **Genres:** A list of movie genres that the user is interested in (e.g., Action, Comedy, Drama, Sci-Fi, Horror, Fantasy, Animation, Anime, Donghua).
     - **Genre Selection Method:** A choice between "AND" (requiring all selected genres to be present in the recommendations) or "OR" (allowing any selected genre to appear in the recommendations).
   - **Optional Input:**
     - **Favorite Movies:** A list of movies the user has enjoyed in the past.
     - **Favorite Books, Series, Games:** Titles that the user likes, which could influence thematic preferences.
     - **IMDb and Rotten Tomatoes Scores:** Minimum acceptable ratings to filter out less favorable movies.
     - **Age Rating:** User's preferred movie rating for appropriate content.
     - **Release Year Range:** The desired time frame for the movie's release.
     - **Preferred Directors:** Specific directors whose work the user favors.

2. **Preference Matching and Recommendation Filtering:**
   - The model uses the parsed input to match user preferences with an extensive database of movies.
   - If the genre selection method is "AND," the model filters for movies that include all specified genres.
   - If the genre selection method is "OR," the model broadens its search to include any movie that matches at least one of the selected genres.
   - Additional filters are applied based on optional input, such as minimum IMDb scores, specific release years, or preferred directors.

3. **Recommendation Generation:**
   - Generate a list of 5 highly relevant movie recommendations that align with the user's preferences.
   - Each recommendation should include:
     - **Movie Title**
     - **Genres**
     - **IMDb Score**
     - **Duration (Runtime)**
     - **Country of Production**
     - **General Plot Summary**
     - **IMDb Link**
     - **Reason for Recommendation:** A brief explanation of why the movie fits the user's specified criteria, considering both mandatory and optional inputs.

4. **Output Formatting and Presentation:**
   - Present the movie recommendations in a clear, tabular format for easy readability.
   - Ensure each movie recommendation is accompanied by all relevant metadata, and provide clickable IMDb links for further exploration.
   - The output should be concise yet informative, offering enough detail to help the user make an informed decision on which movie to watch next.

5. **Performance Optimization:**
   - Optimize model performance through techniques such as hyperparameter tuning, model pruning, and quantization.
   - Ensure the model runs efficiently on standard user devices, providing real-time recommendations with minimal latency.

6. **Explainability and Ethical Considerations:**
   - Include explainability features, using methods like SHAP or LIME, to provide insights into why specific movies were recommended.
   - Address ethical AI considerations, such as avoiding biased recommendations and ensuring diversity in movie suggestions.
   - Support human-in-the-loop feedback for continuous improvement, allowing users to refine recommendations based on their preferences and feedback.

### Output Requirements

Your output should include a well-structured, user-friendly table containing the recommended movies along with all specified details. Each movie should have a reason for its recommendation based on the user’s provided preferences. Ensure the recommendations are diverse, accurate, and tailored to maximize user engagement and satisfaction.

By following these instructions, you will create a model that significantly enhances the movie recommendation process, providing personalized, high-quality suggestions that meet users' unique preferences and needs.

## Installation

To set up the Moviest application, follow these steps:

1. **Clone the Repository:**
```
git clone https://github.com/yourusername/moviest.git
cd moviest
```
2. **Create a Virtual Environment:**
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. **Install the Required Dependencies:**
```
pip install -r requirements.txt
```
4. **Set Up OpenAI API Key:**
```
# api_key.py
openai_api_key = "your_openai_api_key_here"
```
5. **Run the Application:**
```
streamlit run app.py
```

## Useage

Moviest allows users to input their preferences for movie genres and additional optional details like favorite movies, books, IMDb scores, etc. The model will then generate a list of 5 personalized movie recommendations with detailed information.

- Select Movie Genres: Choose from a list of genres you are interested in.
- Choose Genre Selection Method: Decide whether the recommendations should match all selected genres ("AND") or any selected genre ("OR").
- Provide Optional Details: Enter any additional preferences such as favorite movies, books, series, or specific ratings.
- Get Recommendations: Click the "Get Recommendations" button to receive a list of movies tailored to your preferences.

## Example Output
For a visual representation of the application, including its layout and interface, please refer to the [example output](https://github.com/kgeckin/UP-School-AI-First-Developer/blob/3eeb90c8e18c303be32ec2d1693e84afdfaab03a/Moviest/app%20%C2%B7%20Streamlit.pdf). 

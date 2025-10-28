News_Recommendation_Prompt_Chinese = """
    You serve as a personalized news recommendation system. Based on the user’s news history(Chinese title),
    think step by step and recommend candidate news articles(Chinese News).Observe the Output Format to give the answer.
    

    # Input:
    ## User’s History News Title: ${}
    ## Candidate News Title: ${}

    # Task Description:
    1. ’User’s History News’ features headlines that
    have previously engaged the user, signaling
    their interests.
    2. ’Candidate News’ presents a set of headlines
    not yet seen by the user. The sequence of these
    headlines should not influence the ranking.
    3. Your objective is to select the top 10
    headlines from ’Candidate News’ that most
    closely resonate with the user’s interests as
    reflected in ’User’s History News’.

    # Recommendation Process:
    1. Independently assess ’User’s History News’
    to deduce the user’s core interested topics.
    2. Scrutinize the topics of ’Candidate News’,
    disregarding their initial order, to gauge their
    relevance to the user’s interests.
    3. Strategically rank the ’Candidate News’
    headlines by relevance, not by their original
    placement in the list.

    # Output Format
    - Rank candidate news based on the user’s
    history news.Follow this temple: 
    "Ranked news:
    <START>C#, C#, C#, C#, C#, C#, C#, C#, C#,
    C#<END>".
    "Recommend news:
    C#:<Title>:<Explation>
    Recommend news end"
    - Focusing on the alignment of topics rather than
    
    # Warning
    - 1.In your answer, please do not include "Based on the user's history..." etc., but rather give the recommended news headlines directly in the format, thanks!
    - 2.Both <title> and <Exploration> are just placeholders and shouldn't be in the recommended list, they should be replaced with the corresponding title and explanation
    - 3.Don't forget C#.
    - 4.Recommended news must follow the format: C#:<Title>:<Explation>
"""

News_Recommendation_Prompt = """
    You serve as a personalized news recommendation system. Based on the user’s news history,
    think step by step and recommend candidate news articles.Observe the Output Format to give the answer.


    # Input:
    ## User’s History News Title: ${}
    ## Candidate News Title: ${}

    # Task Description:
    1. ’User’s History News’ features headlines that
    have previously engaged the user, signaling
    their interests.
    2. ’Candidate News’ presents a set of headlines
    not yet seen by the user. The sequence of these
    headlines should not influence the ranking.
    3. Your objective is to select the top 10
    headlines from ’Candidate News’ that most
    closely resonate with the user’s interests as
    reflected in ’User’s History News’.

    # Recommendation Process:
    1. Independently assess ’User’s History News’
    to deduce the user’s core interested topics.
    2. Scrutinize the topics of ’Candidate News’,
    disregarding their initial order, to gauge their
    relevance to the user’s interests.
    3. Strategically rank the ’Candidate News’
    headlines by relevance, not by their original
    placement in the list.

    # Output Format
    - Rank candidate news based on the user’s
    history news.Follow this temple: 
    "Ranked news:
    <START>C#, C#, C#, C#, C#, C#, C#, C#, C#,
    C#<END>".
    "Recommend news:
    C#:<Title>:<Explation>
    Recommend news end"
    - Focusing on the alignment of topics rather than

    # Warning
    - 1.In your answer, please do not include "Based on the user's history..." etc., but rather give the recommended news headlines directly in the format, thanks!
    - 2.Both <title> and <Exploration> are just placeholders and shouldn't be in the recommended list, they should be replaced with the corresponding title and explanation
    - 3.Don't forget C#.
    - 4.Recommended news must follow the format: C#:<Title>:<Explation>
"""


Category_PROMPT = """
                You are now a professional news analyst. Please categorize the news by reading the news.
                Please read the following news and choose one of the nine categories: Economy, Real estate, Military, Education, Social, Technology, Entertainment, Internet.
                If you cannot find a suitable category from these eight categories, please categorize the news as Public.
                Input:
                [News]:

                Output:
                [Category]:

                Warning:
                1. Note that [Category] can't be empty, it can only be the eleven categories I mentioned above or the public category, if you can't analyze the category, please set it according to the correspondence of Public
                2. Please follow the Output format defined above, which must contain the characters [Category]:.
                """

News_summary_prompt_zh = '''
    You serve as a personalized news summary generation system. Based on the user's news history, 
    gradually think about and generate summaries(Chinese News Summary) of candidate news contents,
    and generate summaries(Chinese News Summary) that pay more attention to the user's interests.
    # Task Description
    The goal is to analyze the ’User’s History News’
    to understand the user’s past interests and then
    generate summary from ’Candidate News’. The generation of summary should focus more on 
    the user's interest and ignore the information that the user is not interested in.. 
    The task is to analyze the user's interest points based on the ’User’s History News’ and 
    generate a personalized summary for the ’Candidate News’.
    history.
    # Summary Process
    1. Analyze ’User’s History News’ to extract
    keywords and summarize the user’s interests.
    2. Group keywords by meaning to form
    "Topics" that represent related concepts the user
    is interested in.
    3. Extract keywords from ’Candidate News’
    and evaluate how well they match the user’s
    topics of interest.
    4.Generate summaries based on semantic relevance to user interests 
    while disregarding other information in the news
    # Input
    ## User’s History News
    ${}
    ## Candidate News
    ${}
    # Output Format
    [Summary]:
   
   Warning:
   - 1.In your answer, please do not include "Here is the personalized..." etc., but rather give the summary directly in the format, thanks!
   - 2.Please follow the Output format defined above, which must contain the characters [Summary]:
   - 3.Please do not include extra punctuation such as single and double quotes!

'''

News_summary_prompt = '''
    You serve as a personalized news summary generation system. Based on the user's news history, 
    gradually think about and generate summaries of candidate news contents,
    and generate summaries that pay more attention to the user's interests.
    # Task Description
    The goal is to analyze the ’User’s History News’
    to understand the user’s past interests and then
    generate summary from ’Candidate News’. The generation of summary should focus more on 
    the user's interest and ignore the information that the user is not interested in.. 
    The task is to analyze the user's interest points based on the ’User’s History News’ and 
    generate a personalized summary for the ’Candidate News’.
    history.
    # Summary Process
    1. Analyze ’User’s History News’ to extract
    keywords and summarize the user’s interests.
    2. Group keywords by meaning to form
    "Topics" that represent related concepts the user
    is interested in.
    3. Extract keywords from ’Candidate News’
    and evaluate how well they match the user’s
    topics of interest.
    4.Generate summaries based on semantic relevance to user interests 
    while disregarding other information in the news
    # Input
    ## User’s History News
    ${}
    ## Candidate News
    ${}
    # Output Format
    [Summary]:

   Warning:
   - 1.In your answer, please do not include "Here is the personalized..." etc., but rather give the summary directly in the format, thanks!
   - 2.Please follow the Output format defined above, which must contain the characters [Summary]:
   - 3.Please do not include extra punctuation such as single and double quotes!

'''
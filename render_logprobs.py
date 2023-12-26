from IPython.display import HTML, display
import matplotlib.colors as mcolors
from math import exp
from typing import List, Dict

def render_logprobs(sample_data: List[Dict], input_text: str = "", min_logprob: float = -0.5, max_logprob: float = 0, lightness_scale: float = 0.8):
    """
    Render tokens with log probabilities and converted probabilities as HTML

    Args:
        sample_data: List of dicts of token:log probability key value pairs
        input_text: Input text to display above the tokens
        min_logprob: Minimum log probability for color mapping 
        max_logprob: Maximum log probability for color mapping
        lightness_scale: Scale to make the colors lighter - helps text readability
    """


    # Convert logprob to color
    def logprob_to_color(logprob):
        norm = mcolors.Normalize(vmin=min_logprob, vmax=max_logprob)
        if logprob < min_logprob:
            return mcolors.to_hex((1-lightness_scale, 1-lightness_scale, 1))
        else:
            # Generating a blue color with varying intensity - darker for lower probabilities
            intensity = ((norm(logprob)-1)*lightness_scale )+1
            blue_color = (intensity, intensity, 1)  # Darker blue for lower probabilities
            return mcolors.to_hex(blue_color)

    ## CSS
    html_content = """
    <style>
    .token-container {
        display: inline-block;
        margin-right: 2px;
        padding: 2px 4px;
        border-radius: 4px;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        position: relative;
        text-align: center;  /* Center text horizontally */
        vertical-align: middle;  /* Center text vertically */
        line-height: normal;  /* Ensure normal line height for text */
    }

    .token-container .token {
        display: inline-block;
        min-width: 1em;  /* Ensures even space and punctuation have width */
    }

    .token-container .tooltiptext {
        visibility: hidden;
        min-width: 120px; /* Minimum width, but can expand */
        max-width: 600px; /* Maximum width to prevent excessively long tooltips */
        white-space: nowrap; /* Prevents text from wrapping to the next line */
        overflow: hidden; /* Hide overflow */
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 100%; /* Position just below the token */
        left: 50%;
        transform: translateX(-50%); /* Center the tooltip */
        opacity: 0;
        transition: opacity 0.3s;
    }

    .token-container:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """

    ## Input text HTML
    html_content += """
    <p style="font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px;">{}</p>
    <p style="font-family: Arial, sans-serif; ...">
    """.format(input_text) if input_text else ""


    ## Logprobs HTML
    html_content += """<p style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #212121;">"""
    for token_logprobs in sample_data:
        # Get dict element with largest value from token_logprobs
        top_token, top_logprob = max(token_logprobs.items(), key=lambda k: k[1])
        
        color = logprob_to_color(top_logprob) if isinstance(top_logprob, float) else "#ffffff"
        tooltip_text = "<br>".join([f"{token}: {logprob:.4f} ({round(exp(logprob),2)})" for token, logprob in token_logprobs.items()])
        html_content += f'<span class="token-container" style="background-color: {color};"><span class="token">{top_token}</span><span class="tooltiptext">{tooltip_text}</span></span>'

    # print(html_content)
    display(HTML("<br>"+html_content))

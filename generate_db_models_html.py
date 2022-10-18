# pip install html5print requests huggingface-hub Pillow

import argparse
import datetime
import os
import shutil
import sys
from urllib import request as ulreq

import requests
from huggingface_hub import HfApi
from PIL import ImageFile

parser = argparse.ArgumentParser()
parser.add_argument('out_file', nargs='?', help='file to save to', default='stable-diffusion-dreambooth-library.html')
args = parser.parse_args()

print('Will save to file:', args.out_file)

# Init some stuff before saving the time
api = HfApi()
models_list = []

# Save the time now before we do the hard work
dt = datetime.datetime.now()
tz = dt.astimezone().tzname()

# Get list of models under the sd-dreambooth-library organization
for model in api.list_models(author="sd-dreambooth-library"):
    models_list.append(model.modelId.replace('sd-dreambooth-library/', ''))
models_list.sort()

html_struct = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Stable Diffusion DreamBooth Models</title>
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
  <meta http-equiv="Pragma" content="no-cache" />
  <meta http-equiv="Expires" content="0" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="google-site-verification" content="pgoBH8R__ZWngQ-S3o8xopSpHYROu_0VfoS5VYXB3uw" />

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/styles/default.min.css">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">

  <link rel="apple-touch-icon" sizes="180x180" href="/stable-diffusion-dreambooth-library/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/stable-diffusion-dreambooth-library/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/stable-diffusion-dreambooth-library/favicon-16x16.png">
  <link rel="manifest" href="/stable-diffusion-dreambooth-library/site.webmanifest">
  <link rel="mask-icon" href="/stable-diffusion-dreambooth-library/safari-pinned-tab.svg" color="#ee9321">
  <link rel="shortcut icon" href="favicon.ico">
  <meta name="msapplication-TileColor" content="#ee9321">
  <meta name="msapplication-config" content="/stable-diffusion-dreambooth-library/browserconfig.xml">
  <meta name="theme-color" content="#ee9321">

  <!-- Matomo -->
  <!-- Open-source, self hosted, private analytics. No third parties involved. -->
  <script>
    var _paq = window._paq = window._paq || [];
    _paq.push(['trackPageView']);
    _paq.push(['trackVisibleContentImpressions']);
    _paq.push(['enableLinkTracking']);
    _paq.push(['enableHeartBeatTimer']);
    (function() {{
        var u = "https://mato.evulid.cc/";
        _paq.push(['setTrackerUrl', u + 'matomo.php']);
        _paq.push(['setSiteId', '1']);
        var d = document,
          g = d.createElement('script'),
          s = d.getElementsByTagName('script')[0];
        g.async = true;
        g.src = u + 'matomo.js';
        s.parentNode.insertBefore(g, s);
      }})();
  </script>
  <!-- End Matomo Code -->
</head>

<body>
  <style>
    .thumbnail {{
        max-width: 185px;
        display: block;
        padding-top: 5px;
        padding-bottom: 5px;
      }}

    .dreambooth-model-title {{
        margin-top: 100px;
      }}

    body {{
        background-color: #5cff0005 !important;
    }}

    .modal-open {{
    overflow: hidden !important;
    }}

    .close:not(:disabled):not(.disabled) {{
      cursor: pointer;
    }}
    .modal-header .close {{
      padding: 1rem;
      margin: -1rem -1rem -1rem auto;
    }}
    button.close {{
      padding: 0;
      background-color: transparent;
      border: 0;
      -webkit-appearance: none;
    }}
    [type="reset"], [type="submit"], button, html [type="button"] {{
      -webkit-appearance: button;
    }}
    .close {{
      float: right;
      font-size: 1.5rem;
      font-weight: 700;
      line-height: 1;
      color: #000;
      text-shadow: 0 1px 0 #fff;
      opacity: .5;
    }}

    code {{
        color: #b51010;
    }}

    .dreambooth-model-title > a {{
        color: initial !important;
        text-decoration: none !important;
    }}
  </style>

    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="background-color:#6c757d42!important;">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <a class="nav-link" href="/stable-diffusion-models/">Models</a>
          <a class="nav-link" href="/stable-diffusion-textual-inversion-models/">Textual Inversion Embeddings</a>
          <a class="nav-link active" aria-current="page" href="/stable-diffusion-dreambooth-library/">DreamBooth Models</a>
          <a class="nav-link" href="/stable-diffusion-models/sdmodels/">sdmodels</a>
        </div>
      </div>
    </div>
  </nav>

  <div class="container" style="margin-bottom: 180px;">
    <div class="jumbotron text-center" style="margin-top: 45px;margin-right: 45px;margin-bottom: 0px;margin-left: 45px;">
      <h1>Stable Diffusion DreamBooth Models</h1>
    </div>
    <div style="text-align: center;margin-bottom: 45px;font-size: 8pt;">
      <p>
        <i>Page updates automatically daily. Last updated <a class="btn-link" style="cursor: pointer;text-decoration: none;" data-toggle="tooltip" data-placement="bottom" title="{dt.strftime(f"%m-%d-%Y %H:%M:%S {tz}")}">{dt.strftime("%A %B %d, %Y")}</a>.</i>
      </p>
    </div>

    <p>
      Browser for the <a href="https://huggingface.co/sd-dreambooth-library">HuggingFace DreamBooth library</a>. There are currently {len(models_list)} DreamBooth models in sd-dreambooth-library.
    </p>

    <p>
      To use these with <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui">AUTOMATIC1111's SD WebUI</a>, you must convert them. Download the archive of the model you want then use <a href="https://gist.github.com/jachiam/8a5c0b607e38fcc585168b90c686eb05">this script</a> to create a .cktp file.
    </p>

    <p>
            Make sure you have <code>git-lfs</code> installed. If not, do <code class="click-element" data-name="sudo apt install git-lfs">sudo apt install git-lfs</code>. You also need to initalize LFS with <code class="click-element" data-name="git lfs install">git lfs install</code>.
    </p>

    <p>
      The images displayed are the inputs, not the outputs. <!-- Want to quickly test concepts? Try the <a href="https://huggingface.co/spaces/sd-concepts-library/stable-diffusion-conceptualizer">Stable Diffusion Conceptualizer</a> on HuggingFace. --><!-- <a href="https://huggingface.co/docs/diffusers/main/en/training/text_inversion">More info on textual inversion.</a>-->
    </p>

    <center>
      <a href="https://github.com/Cyberes/stable-diffusion-dreambooth-library/actions/workflows/generate_static_html.yml"><img src="https://github.com/Cyberes/stable-diffusion-dreambooth-library/actions/workflows/generate_static_html.yml/badge.svg"></a>
    </center>
    <br>
    <hr>
    <noscript><p><img src="https://mato.evulid.cc/matomo.php?idsite=1&rec=1&url=https://cyberes.github.io/stable-diffusion-dreambooth-library" style="border:0;" alt="" /></p></noscript>
"""

i = 1
for model_name in models_list:
    # For testing
    # if i == 4:
    #     break

    print(f'{i}/{len(models_list)} -> {model_name}')

    html_struct = html_struct + f'<div data-track-content data-content-name="{model_name}" data-content-piece="DreamBooth Model Item"><h3 class="dreambooth-model-title" id="{model_name}"><a href="#{model_name}">{model_name}</a></h3>'

    # Get the concept images from the huggingface repo
    restricted = False
    try:
        files = api.list_repo_files(
            repo_id=f'sd-dreambooth-library/{model_name}')
        concept_images = [i for i in files if i.startswith('concept_images/')]
    except requests.exceptions.HTTPError:
        # Sometimes an author will require you to share your contact info to gain access
        restricted = True

    if restricted:
        html_struct = html_struct + f"""
<p>
  {model_name} is restricted and you must share your contact information to view this repository.
  <a type="button" class="btn btn-link" href="https://huggingface.co/sd-dreambooth-library/{model_name}/">View Repository</a>
</p>
        """
    else:
        html_struct = html_struct + f"""
<p>
  <button type="button" class="btn btn-primary" onclick="openModel('{model_name}', 'https://huggingface.co/sd-dreambooth-library/{model_name}/')">Download</button>
  <a type="button" class="btn btn-link" href="https://huggingface.co/sd-dreambooth-library/{model_name}/">View Repository</a>
</p>
<div class="row">
        """

        # Most repos have 3 concept images but some have more or less
        # We gotta make sure only 3 are shown
        img_count = 3
        if len(concept_images) < 3:
            img_count = len(concept_images)

        for x in range(img_count):
            html_struct = html_struct + f"""
<div class="col-sm">
  <!-- <img class="thumbnail mx-auto lazy-load img-fluid" data-src="https://huggingface.co/sd-dreambooth-library/{model_name}/resolve/main/{concept_images[x]}">-->
  <img class="thumbnail mx-auto img-fluid" loading="lazy" src="https://huggingface.co/sd-dreambooth-library/{model_name}/resolve/main/{concept_images[x]}">
</div>
            """
        html_struct = html_struct + '</div></div>'
    i = i + 1

html_struct = html_struct + """
  </div>

<!-- git clone modal -->
<div class="modal fade" id="gitModal" tabindex="-1" role="dialog" aria-labelledby="gitModalLabel" aria-hidden="true" data-content-name="Repository Popup" data-content-piece="Section" data-track-content>
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="gitModalLabel">Modal title</h5>
<button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <code id="modelDownload" class="click-element" data-name="DreamBooth git clone"></code>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

  <script>
    function openModel(name, url) {
      _paq.push(['trackLink', url, 'download']);
      document.getElementById("gitModalLabel").innerHTML = name;
      $("#modelDownload").html(`git clone ${url}`);
      $("#modelDownload").attr("data-name", url);
      $("#gitModal").modal();
    }

    document.addEventListener("DOMContentLoaded", () => {
      // Enable tooltips
      $(function() {
        $('[data-toggle="tooltip"]').tooltip({
          placement: "bottom"
        })
      });

      hljs.highlightAll();

      function matoPush(category, action, name) {
        _paq.push(["trackEvent", category, action, name]);
      }
      $(".click-element").click(function(e) {
        matoPush('Generic Click', 'Element', $(this).attr("data-name"));
      });
    });
  </script>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/highlight.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <!--<script src="/stable-diffusion-dreambooth-library/jquery.waypoints.min.js"></script>-->
</body>
"""

f = open(args.out_file, 'w', encoding='utf-8')
f.write(html_struct)
f.close()

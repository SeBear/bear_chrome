# bear_chrome
 Daddy`s little helper

Developing work instrument based on Selenium, Google Chrome binaries and chromedriver.

Add most common constructions you use while robotically surfing web.

If you do not use Gooogle Chrome, just install it. Else - 
look forward:
<details>
Make sure you <a href="https://stackoverflow.com/questions/54927496/how-to-download-older-versions-of-chrome-from-a-google-official-site">downloaded Chrome binaries</a> 

<p>Older version of Chrome are not publicly available but you can find and download the matching Chromium binaries from the Chromium build server.</p>

<p>To do so follow the procedure below (derived from <a href="https://www.chromium.org/getting-involved/download-chromium" rel="noreferrer">Chromium wiki</a>):</p>

<p><strong>1/ Find the Full Version Number</strong></p>

<p>You can lookup the full version number matching a release  by searching in the <a href="https://chromereleases.googleblog.com/search/label/Stable%20updates" rel="noreferrer">Chrome Releases Blog</a></p>

<p>Example:</p>

<ul>
<li>Searching for <a href="https://www.google.com/search?q=site%3Achromereleases.googleblog.com%20Chrome%2069" rel="noreferrer">"Chrome 69"</a></li>
<li>We find this <a href="https://chromereleases.googleblog.com/2018/09/stable-channel-update-for-desktop.html" rel="noreferrer">Blog Entry</a></li>
<li>That lists the full version number 69.0.3497.81</li>
</ul>

<p><strong>2/ Find the Branch Base Position</strong></p>

<p>Use the <a href="https://omahaproxy.appspot.com/" rel="noreferrer">"Version Information" tool</a> to find a Branch Base Position for the Full Version number.
To do that enter the Full Version Number and press lookup. 
If the version returns an empty Branch Base Position try increment the last component of the version until you get a Branch Base Version.</p>

<p>Example:</p>

<p>Looking up 69.0.3497.81
<a href="https://i.stack.imgur.com/qYhXX.png" rel="noreferrer"><img src="https://i.stack.imgur.com/qYhXX.png" alt="image.png"></a>
retrieves no Branch Base Position</p>

<p>But looking up 69.0.3497.82
<a href="https://i.stack.imgur.com/U3B3M.png" rel="noreferrer"><img src="https://i.stack.imgur.com/U3B3M.png" alt="enter image description here"></a>
retrieves Branch Base Position:  576753</p>

<p><strong>3/ Download the content for Branch Base Position and platform</strong></p>

<p>Then download the content from the url where you replaced your platform and Branch Base Position value.
<a href="https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=" rel="noreferrer">https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=</a>//</p>

<p>Where  is either "Win_x64", "Linux_x64" or "Mac"</p>

<p>Example: </p>

<p>for Chrome 69 on Linux
<a href="https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/576753/" rel="noreferrer">https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/576753/</a></p>
   
</details>

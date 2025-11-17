<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="description" content="A Binary Search Tree (BST) is a specialized type of binary tree in which each vertex can have up to two children. This structure adheres to the BST property, stipulating that every vertex in the left subtree of a given vertex must carry a value smaller than that of the given vertex, and every vertex in the right subtree must carry a value larger. This visualization implements &amp;#39;multiset&amp;#39; property: Although all keys remain distinct integers, information of duplicated integers are stored as a frequency attribute (only shown for keys that appear more than once). For a demonstration, use the Search(7) function to animate the search for a random value within the range of 1 to 99 in the randomly generated BST above.An Adelson-Velskii Landis (AVL) tree is a self-balancing BST that maintains its height within a logarithmic order (O(log N)) relative to the number of vertices (N) present in the AVL tree.">
    <meta name="keywords" content="Binary Search Tree BST Balanced Adelson Velskii Landis AVL Map Set Search Insert Delete Predecessor Successor Inorder VisuAlgo Data Structure Algorithm Visualization Animation Online Learning Tutorial Lecture">
    <!--<meta name="viewport" content="width=device-width, initial-scale=1">--> <!-- note to self: do not use this as my visualization pages not fully responsive yet -->
    <meta name="csrf-token" content="MZUDnINm1oKaTzu2r7f2ZLMT0JysOZNiPJzL2uIN">
    <meta http-equiv="X-UA-Compatible" content="IE=EDGE">
    <meta property="og:image" content="https://visualgo.net/img/png/bst.png">
    <title>Binary Search Tree, AVL Tree - VisuAlgo</title>

    <link rel="icon" href="https://visualgo.net/img/favicon.png" type="image/x-icon">
    <link rel="shortcut icon" href="https://visualgo.net/img/favicon.png" type="image/x-icon">
    <link rel="apple-touch-icon" href="https://visualgo.net/img/favicon.png">
    <link rel="apple-touch-icon" sizes="72x72" href="https://visualgo.net/img/favicon.png">
    <link rel="apple-touch-icon" sizes="114x114" href="https://visualgo.net/img/favicon.png">

    <link rel="stylesheet" href="https://visualgo.net/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="https://visualgo.net/fonts/silkscreen/stylesheet.css">
    <link rel="stylesheet" type="text/css" href="https://visualgo.net/fonts/latinmodern-math/stylesheet.css">
    <link rel="stylesheet" type="text/css" href="https://visualgo.net/css/common-1.0.2.css">
        <link rel="stylesheet" href="https://visualgo.net/css/viz-1.0.5.css">
    <link rel="stylesheet" href="https://visualgo.net/css/visual.css">
    <link rel="stylesheet" href="https://visualgo.net/css/drawgraph-1.0.2.css">
    <style>
      #e-lecture {
        top: 45px;
        right: 130px;
        width: 400px;
        display: block;
        background: none;
        /*overflow: normal;*/
        white-space: normal;
        text-align: right;
        color: black; font-weight: bold; font-size: 20px;
        z-index: 8001;
      }
      #e-lecture-timeline {
        top: 80px;
        right: 130px;
        display: flex;
        position: absolute;
        z-index: 10000;
      }
      .e-lecture-timeline-slide {
        height: 5px;
        width: 2px;
        background: black;
        float: left;
      }
      .e-lecture-timeline-checkpoint {
        height: 20px;
        width: 3px;
        margin-left: 2px;
        margin-top: -7.5px;
        background: black;
        float: left;
      }

      #e-lecture-f1map {
        top: 102.5px;
        right: 130px;
        display: flex;
        position: absolute;
        z-index: 10000;
      }

      .e-lecture-f1map-sector {
        flex-grow: 1;
        background: black;
        float: left;
        height: 5px;
        margin-right: 1px;
      }

      .e-lecture-f1map-sector:last-child {
        margin-right: 0px;
      }

      .electure-prev, .electure-next { /* force update, copied from viz.css */
        position: absolute;
        /* bottom: -12px; */
        top: -20px;
        /*bottom: '';*/
        padding: 3px 8px;
        background: #999;
        color: white;
        cursor: pointer;
        border-radius: 2px;
      }

      .electure-read-status {
        position: absolute;
        bottom: 4px;
        right: 4px;
        font-size: 14px;
        cursor: default;
        color: #00FF7F;
        display: none;
      }

      .electure-prev {
        left: -10px;
        /* right: 30px; */
      }
      .electure-next {
        right: -10px;
        color: white;
      }
      .electure-print, .electure-end {
        position: fixed;
        top: 45px;
        height: 20px;
        width: 17px;
        right: 80px;
        padding: 3px 8px;
        background: #999;
        color: white;
        cursor: pointer;
        border-radius: 2px;
        text-align: center;
      }
      .electure-end {
        right: 45px; /* beside the X */
      }

      #change-lang-popup {
        position: fixed;
        background: green;
        left: 40px;
        top: 50px;
        width: 250px;
        height: 125px;
        border: transparent;
        border-radius: 10px;
        padding: 10px 20px;
        z-index: 9000;
      }

      #change-lang-popup p {
        font-size: medium;
        color: white;
        line-height: 2;
        font-family: "PT Sans", sans-serif;
      }

      #change-lang-popup-btn {
        text-decoration: underline;
        margin-left: 50px;
      }

      #change-lang-popup-btn:hover {
        cursor: pointer;
      }

      #rotateDeviceOverlay {
        z-index: 10000;
        width: 90%;
        height: 100%;
        align-items: center;
        justify-content: center;
        background-color: white;
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        right: 0;
        display: flex;
        padding-right: 5%;
        padding-left: 5%;
        overflow: hidden;
      }

      #mobile-playback-overlay {
        z-index: 9600;
        width: 90%;
        height: 100%;
        align-items: center;
        justify-content: center;
        gap: 100px;
        background-color: black;
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        right: 0;
        display: flex;
        padding-right: 5%;
        padding-left: 5%;
        opacity: 0.3;
        overflow: hidden;
      }
      .mobile-playback-item {
        min-width: 2.5%;
        max-width: 35px;
      }
      .mobile-playback-item img {
        width: 100%
      }
      .mobile-playback-label {
        opacity: 0;
        color: white;
        font-size: 25px;
        font-weight: bold;
        min-width: 1.5%;
        max-width: 25px;
        transition: opacity 0.25s ease-out;
        -webkit-backface-visibility: hidden;
      }
      #mobile-playback-rewind-label {
        margin-right: -70px;
      }
      #mobile-playback-forward-label {
        margin-left: -70px;
      }
      #viz-speed-value {
          font-size: 15px;
          width: 10%;
      }

      #scale {
        position: fixed;
        left: 5px;
      }

      #status-for-embed {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 45px;
        text-align: center;
        color: white;
        font-size: 1.2em;
        overflow: clip;
      }
    </style>
    
    <style>
/* copied here from common.css (perhaps need to use version numbering) until caches worldwide settles */
#reload-mobile-popup, #message-popup { /* #gdpr-popup, */
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  min-width: 320px;
  bottom: 62px;
  height: 300px;
  background-color: #0275d8;
  border-radius: 15px;
  padding: 30px 40px;
  z-index: 9500;
}
#reload-mobile-popup {
  background-color: green;
  height: 200px;
}
#message-popup {
  z-index: 9000;
  width: 40%;
  height: 130px;
  background-color: #d9534f;
}

#reload-mobile-popup p, #message-popup p { /* #gdpr-popup p, */
  font-size: large;
  color: white;
  line-height: 2;
  font-family: "PT Sans", sans-serif;
}

#reload-mobile-popup .inner-button, #message-popup .inner-button { /* #gdpr-popup .gdpr-button, */
  border: white solid 2px;
  border-radius: 4px;
  font-weight: bold;
  font-size: x-large;
  padding: 2px 8px;
  color: white;
  width: 90px;
  text-align: center;
  position: absolute;
  letter-spacing: 1px;
  text-decoration: none;
  cursor: pointer;
}

#gdpr-accept, #reload-mobile-button, #dismiss-message-btn {
  bottom: 30px;
  right: 40px;
}

#gdpr-reject, #cancel-reload-mobile-button {
  bottom: 30px;
  right: 170px;
}

#alert-container {
  position: absolute;
  top: 60px;
  left: 60px;
  z-index: 10;

  width: 300px;

  display: flex;
  flex-direction: column;
}


.alert {
  padding: 10px;
  background-color: #f44336;
  color: white;
  opacity: 1;
  transition: opacity 0.6s;
  margin-bottom: 8px;
  flex: 1;
}

.alert.success {background-color: #04AA6D;}
.alert.info {background-color: #2196F3;}
.alert.warning {background-color: #ff9800;}

.closebtn {
  margin-left: 15px;
  color: white;
  font-weight: bold;
  float: right;
  font-size: 22px;
  line-height: 20px;
  cursor: pointer;
  transition: 0.3s;
}

.closebtn:hover {
  color: black;
}
    </style>
  </head>

  <body>
    <div id="body-container" style="display: flex; flex-direction: column; min-height: 100vh;">
        <style>
  #topbar {
    background-color: rgb(0,0,0);
    font-family: "PT Sans", sans-serif;
    font-size: 13px;
    height: 40px;

    padding-left: 40px;
    padding-right: 40px;

    display: flex;
    flex-wrap: wrap;
    align-items: center;
    position: relative;
    justify-content: flex-start;
  }

  #topbar a:hover {
    text-decoration: none;
  }

  #account-dropdown-btn {
    color: #198754;
    font-size: 1rem;
    padding: 0 0.5rem;
    margin-left: 0.5rem;

    border: 2px solid;
    border-radius: 0.25rem;
    height: 24px;
    line-height: 1.5;
  }

  #account-dropdown-btn:hover {
    color: #0a58ca!important;
    border-color: #198754;
    text-decoration: none;
  }

  #login-button {
    color: #198754;
    font-size: 1rem;
    padding: 0 0.5rem;
    margin-left: 0.5rem;

    border: 2px solid;
    border-radius: 0.25rem;

    height: 24px;
    line-height: 1.5;
  }

  #login-button a:hover {
    color: #0a58ca!important;
    text-decoration: none;
  }

  #account-dropdown-menu {
    display: none;
    position: absolute;
    background-color: white;
    z-index: 1000;
    min-width: 10rem;
    padding: 0.5rem 0;
    margin: 0;
    font-size: 1rem;
    color: rgb(0,0,0);
    text-align: left;
    list-style: none;
    background-clip: padding-box;
    border: 1px solid rgba(0,0,0,.15);
    border-radius: 0.25rem;
    top: 45px;
    right: 40px;
    line-height: 1.5;
  }

  .account-dropdown-item {
    display: block;
    width: auto;
    padding: 0.25rem 1rem;
    clear: both;
    font-weight: 400;
    color: rgb(0,0,0);
    text-align: inherit;
    text-decoration: none;
    white-space: nowrap;
    background-color: transparent;
    border: 0;
    height: 24px;
    font-family: SilkscreenNormal, sans-serif;
  }

  .account-dropdown-item:hover {
    background-color: #e9ecef;
    color: #0a58ca;
    text-decoration: none;
  }
</style>

<nav id="topbar">
  <span style="margin-right: 0.25rem">
    <a href="https://www.comp.nus.edu.sg/~stevenha" style="text-decoration: none; color: white">
      <span class="colour" style="border: 1px solid; border-color: #198754!important; border-radius: .25rem!important">7</span>
    </a>
    <a href="https://visualgo.net" style="font-family: SilkscreenNormal,sans-serif; font-size: 20px; margin-left: 4px;">
      <span style="color: white">Visu</span><span class="colour">Algo</span><span style="font-size: 40%; color: white">.net</span>
    </a>
          <span style="color: white">/</span>
      <select id="Language" class="select2-dropdown" onchange="changeURL()">
                  <option value="en" selected>en</option>
                  <option value="zh" >zh</option>
                  <option value="id" >id</option>
              </select>
              <span style="color: white; font-family: monospace">/bst</span>
      </span>

  <span style="max-height: 30px">
    <span id="title">
              <a id='title-BST'  class='selected-viz'>Binary Search Tree</a>
              <a id='title-AVL' >AVL Tree</a>
          </span>
  </span>

  <span style="max-height: 30px; background-color:rgb(0,0,0)!important; color: white; margin-left: auto">
    <div id="mode-menu">
        <div id='mode-button' style="background-color: rgb(0,0,0)!important;" title='exploration'>Exploration Mode &#9663;</div>
        <div id='other-modes' style="background-color: rgb(0,0,0)!important; padding-top: 11px">
          <a title='e-Lecture' style="background-color: rgb(0,0,0)!important;">e-Lecture Mode</a> 
        </div>
      </div>
  </span>

      <span id="login-button" style="font-family: SilkscreenNormal,sans-serif">
      <a href="https://visualgo.net/login">Login</a>
    </span>
  </nav>

<ul id="account-dropdown-menu">
  <li><a class="account-dropdown-item" href="https://visualgo.net/profile">Profile</a></li>
  <li><a class="account-dropdown-item" href="https://visualgo.net/training">Training</a></li>
  <li><a class="account-dropdown-item" href="https://visualgo.net/tests">Tests</a></li>
      <li><a class="account-dropdown-item" href="https://visualgo.net/logout">Log Out</a></li>
</ul>

<script>
  function changeURL() {
    let URL = window.location.href.split('/');
    URL[3] = document.getElementById("Language").value;
    window.location.assign(URL.join('/'));
  }

  function changeDefaultLanguageAndURL() {
    let URL = window.location.href.split('/');
    let val = document.getElementById("Language").value;
    URL[3] = val;

    let data = {
      '_token': "MZUDnINm1oKaTzu2r7f2ZLMT0JysOZNiPJzL2uIN",
      'lang'  : val
    }
    $.post('https://visualgo.net/changeLanguage', data, function (res, status) {
      if(res['status'] === 'success') {
        window.location.assign(URL.join('/'));
      } else if (res['status'] === 'failed') {
        alert(res['message']);
      } else {
        alert('An unknown error occurred');
      }
    })
  }
</script>

      <div id="alert-container">
      </div>

      <div id="dark-overlay"></div>

      <div id="main-content-container" style="flex: 1">
        <!-- 4 Jan 2022: Manas, img/arrow_white_right.png is still here -->
    <div id="mobile-playback-overlay" class="playing" style="display: none;">
      <span id="mobile-playback-rewind-label" class="mobile-playback-label">-7</span>
      <span id="mobile-playback-rewind" class="mobile-playback-item" onclick=mobilePlaybackRewind()><img src="https://visualgo.net/img/prevFrame.png" alt="rewind 7 frames"></span>
      <span id="mobile-playback-pause" class="mobile-playback-item" onclick=mobilePlaybackPauseOrPlay()><img src="https://visualgo.net/img/pause.png" alt="pause"></span>
      <span id="mobile-playback-play" class="mobile-playback-item" style="display: none;" onclick=mobilePlaybackPauseOrPlay()><img src="https://visualgo.net/img/play.png" alt="play"></span>
      <span id="mobile-playback-forward" class="mobile-playback-item" onclick=mobilePlaybackForward()><img src="https://visualgo.net/img/nextFrame.png" alt="forward 7 frames"></span>
      <span id="mobile-playback-forward-label" class="mobile-playback-label">+7</span>
    </div>
    <div id="status" class="panel"><p></p></div>
    <div id="status-hide" class="panel-hide unselectable"><img src="https://visualgo.net/img/arrow_white_right.png" alt=">" title="show/hide status panel"/></div>

    <div id="codetrace" class="panel">
      <p id="code1" style="padding-top: 10px;"></p>
      <p id="code2"></p>
      <p id="code3"></p>
      <p id="code4"></p>
      <p id="code5"></p>
      <p id="code6"></p>
      <p id="code7" style="padding-bottom: 10px;"></p>
    </div>
    <div id="codetrace-hide" class="panel-hide unselectable"><img src="https://visualgo.net/img/arrow_white_right.png" alt=">" title="show/hide codetrace panel"/></div>
    <div id="status-for-embed" class="show-if-embed unselectable" style="display: none;">
      <p></p>
    </div>

    <div id="left-bar"></div>
    <div id="right-bar"></div>

    <div id="media-controls">
    <div id='speed-control'><div id='speed-input'></div><div id='viz-speed-value'>1x</div></div>
      <span id="go-to-beginning" class="media-control-button" title="go to beginning" onclick=goToBeginning()><img src="https://visualgo.net/img/goToBeginning.png" alt="go to beginning"></span>
      <span id="previous" class="media-control-button" title="step backward" onclick=stepBackward()><img src="https://visualgo.net/img/prevFrame.png" alt="previous frame"></span>
      <span id="pause" class="media-control-button" title="pause" onclick=pause()><img src="https://visualgo.net/img/pause.png" alt="pause"></span>
      <span id="play" class="media-control-button" title="play" onclick=play()><img src="https://visualgo.net/img/play.png" alt="play"></span>
      <span id="next" class="media-control-button" title="step forward" onclick=stepForward()><img src="https://visualgo.net/img/nextFrame.png" alt="next frame"></span>
      <span id="go-to-end" class="media-control-button" title="go to end" onclick=goToEnd()><img src="https://visualgo.net/img/goToEnd.png" alt="go to end"></span>
      <div id="progress-bar" class="media-control-button"></div>
    </div>

    <div id='viz'>
       <p id="info"></p>
    </div>
    <div id='current-action-toggle' class="hide-if-embed">
      <div id='current-action' class='panel'></div>
    </div>

    <div id='e-lecture' class='panel'></div> <!-- to do soon: put all that have to appear/disappear together when div with id overlay is shown/hide, respectively -->
    <div id='e-lecture-timeline'></div>
    <div id='e-lecture-f1map'>
      <div class="e-lecture-f1map-sector" sectorNo=1></div>
      <div class="e-lecture-f1map-sector" sectorNo=2></div>
      <div class="e-lecture-f1map-sector" sectorNo=3></div>
    </div>
    <div id="overlay" hidden onclick="end_eLecture()"> <!-- Steven add this behavior on 10 Feb 2022, if the dark overlay is clicked/tapped, we go to exploration mode again -->
      <div id='electure-dropdown'>
        <select class="lecture-dropdown" style="width:100%">
                    <option value="1">1. Binary Search Tree</option>
                    <option value="2">2. BST & Balanced BST (AVL Tree)</option>
                    <option value="3">3. Motivation</option>
                    <option value="3-1">&nbsp;&nbsp;&nbsp;3-1. What Kind of Table ADT?</option>
                    <option value="3-2">&nbsp;&nbsp;&nbsp;3-2. Using Unsorted Array/Vector</option>
                    <option value="3-3">&nbsp;&nbsp;&nbsp;3-3. Using Sorted Array/Vector</option>
                    <option value="3-4">&nbsp;&nbsp;&nbsp;3-4. O(log N) Complexities?</option>
                    <option value="3-5">&nbsp;&nbsp;&nbsp;3-5. Other Table ADT Operations</option>
                    <option value="3-6">&nbsp;&nbsp;&nbsp;3-6. The Answer</option>
                    <option value="3-7">&nbsp;&nbsp;&nbsp;3-7. What about Linked List?</option>
                    <option value="3-8">&nbsp;&nbsp;&nbsp;3-8. The Answer</option>
                    <option value="3-9">&nbsp;&nbsp;&nbsp;3-9. What about Hash Table?</option>
                    <option value="3-10">&nbsp;&nbsp;&nbsp;3-10. The Answer</option>
                    <option value="4">4. Visualization</option>
                    <option value="4-1">&nbsp;&nbsp;&nbsp;4-1. BST Vertex Attributes</option>
                    <option value="4-2">&nbsp;&nbsp;&nbsp;4-2. Removing the Parent Pointer</option>
                    <option value="4-3">&nbsp;&nbsp;&nbsp;4-3. BST Property</option>
                    <option value="5">5. BST Operations</option>
                    <option value="5-1">&nbsp;&nbsp;&nbsp;5-1. A Few Other BST Operations</option>
                    <option value="5-2">&nbsp;&nbsp;&nbsp;5-2. Static vs Dynamic Data Structure</option>
                    <option value="6">6. Search(v)</option>
                    <option value="6-1">&nbsp;&nbsp;&nbsp;6-1. lower_bound(v)</option>
                    <option value="6-2">&nbsp;&nbsp;&nbsp;6-2. SearchMin() and SearchMax()</option>
                    <option value="6-3">&nbsp;&nbsp;&nbsp;6-3. O(h) Time Complexity</option>
                    <option value="7">7. Successor(v)</option>
                    <option value="7-1">&nbsp;&nbsp;&nbsp;7-1. Predecessor(v)</option>
                    <option value="7-2">&nbsp;&nbsp;&nbsp;7-2. O(h) Time Complexity</option>
                    <option value="8">8. Inorder Traversal</option>
                    <option value="8-1">&nbsp;&nbsp;&nbsp;8-1. O(N) Time Complexity</option>
                    <option value="8-2">&nbsp;&nbsp;&nbsp;8-2. The Answer</option>
                    <option value="8-3">&nbsp;&nbsp;&nbsp;8-3. Preorder and Postorder Traversal</option>
                    <option value="8-4">&nbsp;&nbsp;&nbsp;8-4. The Answer</option>
                    <option value="9">9. Insert(v)</option>
                    <option value="9-1">&nbsp;&nbsp;&nbsp;9-1. O(h) Time Complexity</option>
                    <option value="9-2">&nbsp;&nbsp;&nbsp;9-2. Mini Quiz</option>
                    <option value="10">10. Remove(v) - Three Possible Cases</option>
                    <option value="10-1">&nbsp;&nbsp;&nbsp;10-1. Remove(v) - Case 1</option>
                    <option value="10-2">&nbsp;&nbsp;&nbsp;10-2. Remove(v) - Case 2</option>
                    <option value="10-3">&nbsp;&nbsp;&nbsp;10-3. Remove(v) - Case 3</option>
                    <option value="10-4">&nbsp;&nbsp;&nbsp;10-4. Remove(v) - Case 3 Discussion</option>
                    <option value="10-5">&nbsp;&nbsp;&nbsp;10-5. The Answer</option>
                    <option value="10-6">&nbsp;&nbsp;&nbsp;10-6. O(h) Time Complexity</option>
                    <option value="11">11. Create BST</option>
                    <option value="12">12. Intermezzo</option>
                    <option value="12-1">&nbsp;&nbsp;&nbsp;12-1. Try Exploration Mode</option>
                    <option value="13">13. Balanced BST</option>
                    <option value="13-1">&nbsp;&nbsp;&nbsp;13-1. AVL Tree</option>
                    <option value="13-2">&nbsp;&nbsp;&nbsp;13-2. Extra BST Attribute: height(v)</option>
                    <option value="13-3">&nbsp;&nbsp;&nbsp;13-3. Formal Definition of height(v)</option>
                    <option value="13-4">&nbsp;&nbsp;&nbsp;13-4. Mini Quiz</option>
                    <option value="13-5">&nbsp;&nbsp;&nbsp;13-5. The Lower Bound of BST Height</option>
                    <option value="13-6">&nbsp;&nbsp;&nbsp;13-6. Derivation of the Lower Bound</option>
                    <option value="13-7">&nbsp;&nbsp;&nbsp;13-7. The Upper Bound of BST Height</option>
                    <option value="13-8">&nbsp;&nbsp;&nbsp;13-8. The Solution</option>
                    <option value="13-9">&nbsp;&nbsp;&nbsp;13-9. The Combined Bound</option>
                    <option value="14">14. AVL Tree</option>
                    <option value="14-1">&nbsp;&nbsp;&nbsp;14-1. Step 1: Maintaining height(v) Efficiently</option>
                    <option value="14-2">&nbsp;&nbsp;&nbsp;14-2. Step 2: Define AVL Tree Invariant</option>
                    <option value="14-3">&nbsp;&nbsp;&nbsp;14-3. Proof - 1</option>
                    <option value="14-4">&nbsp;&nbsp;&nbsp;14-4. Proof - 2</option>
                    <option value="14-5">&nbsp;&nbsp;&nbsp;14-5. Proof - 3</option>
                    <option value="14-6">&nbsp;&nbsp;&nbsp;14-6. Proof - 4</option>
                    <option value="14-7">&nbsp;&nbsp;&nbsp;14-7. Step 3: Maintain Invariant</option>
                    <option value="14-8">&nbsp;&nbsp;&nbsp;14-8. Introducing Tree Rotation</option>
                    <option value="14-9">&nbsp;&nbsp;&nbsp;14-9. Non-trivial O(1) Tree Rotation Pseudo-code</option>
                    <option value="14-10">&nbsp;&nbsp;&nbsp;14-10. Four Rebalancing Cases</option>
                    <option value="14-11">&nbsp;&nbsp;&nbsp;14-11. Insert(v) in AVL Tree</option>
                    <option value="14-12">&nbsp;&nbsp;&nbsp;14-12. The Answer</option>
                    <option value="14-13">&nbsp;&nbsp;&nbsp;14-13. Remove(v) in AVL Tree</option>
                    <option value="14-14">&nbsp;&nbsp;&nbsp;14-14. AVL Tree Summary</option>
                    <option value="15">15. Extras</option>
                    <option value="15-1">&nbsp;&nbsp;&nbsp;15-1. Those 2 Extra BST Operations</option>
                    <option value="15-2">&nbsp;&nbsp;&nbsp;15-2. Side Usage of Balanced BST?</option>
                    <option value="15-3">&nbsp;&nbsp;&nbsp;15-3. Online Quiz</option>
                    <option value="15-4">&nbsp;&nbsp;&nbsp;15-4. Online Judge Exercises</option>
                    <option value="15-5">&nbsp;&nbsp;&nbsp;15-5. The Solution</option>
                  </select>
      </div>

      <div class='electure-print' title='Print the e-Lecture note' style='z-index=8001;'>&#9997;</div>

      <div class='electure-end' title='Close the e-Lecture mode' style='z-index=8001;'>&#10008;</div>
    </div>

    <div id="dropdown-temp-holder" hidden></div>

<!-- Steven's proper fix on 28 Jan 2022, to remove the last 4 slides about 99, 99-1, 99-2, and 99-3 that are added in app/Helpers/VizPageHelper -->
    <div id="electure-1" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>A Binary Search Tree (BST) is a specialized type of binary tree in which each vertex can have up to two children. This structure adheres to the <b>BST property</b>, stipulating that every vertex in the left subtree of a given vertex must carry a value smaller than that of the given vertex, and every vertex in the right subtree must carry a value larger. This visualization implements &#39;multiset&#39; property: Although all keys remain distinct integers, information of duplicated integers are stored as a frequency attribute (only shown for keys that appear more than once). For a demonstration, use the <span class="slide-actions" onclick="doButtonAction1()">Search(7)</span> function to animate the search for a random value within the range of 1 to 99 in the randomly generated BST above.</p><br><p>An Adelson-Velskii Landis (AVL) tree is a <b>self-balancing</b> BST that maintains its height within a logarithmic order (O(log <b>N</b>)) relative to the number of vertices (<b>N</b>) present in the AVL tree.</p>

<div class="electure-addition">
  <hr>
  <p><b>Remarks</b>: By default, we show e-Lecture Mode for first time (or non logged-in) visitor.<br>
  If you are an NUS student and a repeat visitor, please <a href="https://visualgo.net/login"><u>login</u></a>.</p>
</div>


  <div class='electure-next' data-nextid="2" title='Go to the next slide 2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-2" class="electure-dialog" style="top:70px;left:280px;width:500px;">
  <p>To switch between the standard Binary Search Tree and the AVL Tree (which primarily differs during the insertion and removal of an integer), please select the corresponding header.</p><br><p>We also provide a URL shortcut for quick access to the AVL Tree mode, available at <a href="./bst?mode=AVL"><u>https://visualgo.net/en/avl</u></a>. The &#39;en&#39; in the URL can be replaced with the two-character code of your preferred language, if available.</p>

<div class="electure-addition">
  <hr>
  <p>Pro-tip 1: Since you are not <a href="https://visualgo.net/login"><u>logged-in</u></a>, you may be a first time visitor (or not an NUS student) who are not aware of the following keyboard shortcuts to navigate this e-Lecture mode: <b>[PageDown]</b>/<b>[PageUp]</b> to go to the next/previous slide, respectively, (and if the drop-down box is highlighted, you can also use <b>[&rarr; or &darr;/&larr; or &uarr;]</b> to do the same),and <b>[Esc]</b> to toggle between this e-Lecture mode and exploration mode.</p>
</div>

  <div class='electure-prev' data-nextid="1" title='Go to the previous slide 1'>&larr;</div>

  <div class='electure-next' data-nextid="3" title='Go to the next slide 3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>A BST, particularly a balanced BST such as an AVL Tree, is an effective data structure for implementing <i>a certain type</i> of <b>Table</b> (or <b>Map</b>) Abstract Data Type (ADT).</p><br><p>A Table ADT should efficiently support <b>at least</b> the following three operations:</p><ol><li>Search(v) — ascertain whether <b>v</b> exists within the ADT,</li><li>Insert(v) — add <b>v</b> into the ADT,</li><li>Remove(v) — eliminate <b>v</b> from the ADT.</li></ol><hr><p>For a similar discussion, refer to the <a href="https://visualgo.net/en/hashtable?slide=2-1" target="_blank"><u>Hash Table e-Lecture slides</u></a>.</p>

<div class="electure-addition">
  <hr>
  <p>Pro-tip 2: We designed this visualization and this e-Lecture mode to look good on 1366x768 resolution <b>or larger</b> (typical modern laptop resolution in 2021). We recommend using Google Chrome to access VisuAlgo. Go to full screen mode (<b>F11</b>) to enjoy this setup. However, you can use zoom-in (<b>Ctrl +</b>) or zoom-out (<b>Ctrl -</b>) to calibrate this.</p>
</div>

  <div class='electure-prev' data-nextid="2" title='Go to the previous slide 2'>&larr;</div>

  <div class='electure-next' data-nextid="3-1" title='Go to the next slide 3-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-1" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>We are referring to a particular type of Table ADT where the keys must be ordered. This contrasts with other types of Table ADTs that allow for unordered keys.</p><br><p>The specific requirements of this Table ADT type will be clarified in the subsequent slides.</p>

<div class="electure-addition">
  <hr>
  <p>Pro-tip 3: Other than using the typical media UI at the bottom of the page, you can also control the animation playback using keyboard shortcuts (in Exploration Mode): <b>Spacebar</b> to play/pause/replay the animation, <b>&larr;</b>/<b>&rarr;</b> to step the animation backwards/forwards, respectively, and <b>-</b>/<b>+</b> to decrease/increase the animation speed, respectively.</p>
</div>

  <div class='electure-prev' data-nextid="3" title='Go to the previous slide 3'>&larr;</div>

  <div class='electure-next' data-nextid="3-2" title='Go to the next slide 3-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-2" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>Using an <b>unsorted</b> array or vector to implement a Table ADT can result in inefficiencies:</p><ol><li>Search(v) operates in O(<b>N</b>) time complexity because we may need to traverse all <b>N</b> elements of the ADT if <b>v</b> doesn&#39;t exist,</li><li>Insert(v) can be implemented with O(<b>1</b>) time complexity, by simply appending <b>v</b> at the end of the array,</li><li>Remove(v) also runs in O(<b>N</b>) time complexity, as we first need to search for <b>v</b> (which is already O(<b>N</b>)), and then close the gap resulting from the deletion — also an O(<b>N</b>) operation.</li></ol>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-1" title='Go to the previous slide 3-1'>&larr;</div>

  <div class='electure-next' data-nextid="3-3" title='Go to the next slide 3-3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-3" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>Implementing a Table ADT with a <b>sorted</b> array or vector can enhance the performance of Search(v), but this comes at the expense of Insert(v) performance:</p><ol><li>Search(v) can now be implemented with a time complexity of O(log <b>N</b>), as we can employ a binary search strategy on the sorted array,</li><li>Insert(v) now operates with a time complexity of O(<b>N</b>), as we need to use an insertion-sort-like strategy to ensure the array remains sorted,</li><li>Remove(v) still runs in O(<b>N</b>) time complexity. Although Search(v) operates in O(log <b>N</b>), we still have to close the gap resulting from the deletion, which runs in O(<b>N</b>).</li></ol>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-2" title='Go to the previous slide 3-2'>&larr;</div>

  <div class='electure-next' data-nextid="3-4" title='Go to the next slide 3-4'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-4" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>The objective of this e-Lecture is to introduce the BST and the balanced BST data structure, namely the AVL Tree, which enable us to implement basic Table ADT operations like Search(v), Insert(v), and Remove(v) — <b>along with a few other Table ADT operations</b> (refer to the next slide) — in O(log <b>N</b>) time. This time complexity is significantly smaller than <b>N</b>. Please try the interactive slider below to feel the significant difference.</p><br><center><input id="logn_input" type="range" min="0" max="40" value="20"><br><p>log <b>N</b> = <output id="logn">20</output>, <b>N</b> = <output id="n">1048576</output>.</p><br></center><p>PS: More experienced readers may note the existence of <a href="hashtable?slide=11-4"><u>another data structure</u></a> that can perform these three basic Table ADT operations more swiftly. But, keep reading...</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-3" title='Go to the previous slide 3-3'>&larr;</div>

  <div class='electure-next' data-nextid="3-5" title='Go to the next slide 3-5'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-5" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>In addition to the basic three operations, there are several other Table ADT operations:</p><ol><li>Find the Min()/Max() element,</li><li>Find the Successor(v), or the &#39;next larger&#39; element, and Predecessor(v), or the &#39;previous smaller&#39; element,</li><li>List elements in sorted order,</li><li><a href="./bst?slide=5-1"><u>Rank(v) & Select(k)</u></a>,</li><li>There are other possible operations as well.</li></ol><p>Discussion: Given the constraint of using either a sorted or unsorted array/vector, what would be the optimal implementation for the first three additional operations above?</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-4" title='Go to the previous slide 3-4'>&larr;</div>

  <div class='electure-next' data-nextid="3-6" title='Go to the next slide 3-6'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-6" class="electure-dialog" style="top:70px;left:60px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-5" title='Go to the previous slide 3-5'>&larr;</div>

  <div class='electure-next' data-nextid="3-7" title='Go to the next slide 3-7'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-7" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>The simpler data structure that can be used to implement Table ADT is <a href="./list"><u>Linked List</u></a>.</p><br><input class="mcq-answer" id="mcq-answer-16" value="70" hidden><p>Quiz: <b>Can we perform all basic three Table ADT operations: Search(v)/Insert(v)/Remove(v) efficiently (read: faster than O(<b>N</b>)) using Linked List?</b></p><form><input type="radio" name="mcq-16-choice" value="70"> No<br><input type="radio" name="mcq-16-choice" value="69"> Yes<br></form><button class="mcq-submit" id="submit-16">Submit</button> <span id="answer-status-16"></span><br><br><p>Discussion: Why?</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-6" title='Go to the previous slide 3-6'>&larr;</div>

  <div class='electure-next' data-nextid="3-8" title='Go to the next slide 3-8'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-8" class="electure-dialog" style="top:70px;left:60px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-7" title='Go to the previous slide 3-7'>&larr;</div>

  <div class='electure-next' data-nextid="3-9" title='Go to the next slide 3-9'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-9" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>Another data structure that can be used to implement Table ADT is <a href="./hashtable"><u>Hash Table</u></a>. It has very fast Search(v), Insert(v), and Remove(v) performance (all in expected O(<b>1</b>) time).</p><br><input class="mcq-answer" id="mcq-answer-17" value="72" hidden><p>Quiz: <b>So what is the point of learning this BST module if Hash Table can do the crucial Table ADT operations in unlikely-to-be-beaten expected O(<b>1</b>) time?</b></p><form><input type="radio" name="mcq-17-choice" value="71"> There is no point, so this BST module can be ignored<br><input type="radio" name="mcq-17-choice" value="72"> There are valid reasons, which are ____<br></form><button class="mcq-submit" id="submit-17">Submit</button> <span id="answer-status-17"></span><br><br><p>Discuss the answer above! Hint: Go back to <a href="./bst?slide=3-5"><u>the previous 4 slides ago</u></a>.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-8" title='Go to the previous slide 3-8'>&larr;</div>

  <div class='electure-next' data-nextid="3-10" title='Go to the next slide 3-10'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-3-10" class="electure-dialog" style="top:70px;left:60px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-9" title='Go to the previous slide 3-9'>&larr;</div>

  <div class='electure-next' data-nextid="4" title='Go to the next slide 4'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-4" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We will now introduce the BST data structure. Refer to the visualization of an example BST provided above!</p><br><p>In a BST, the root vertex is unique and has no parent. Conversely, a leaf vertex, of which there can be several, has no children. Vertices that aren&#39;t leaves are known as internal vertices. Occasionally, the root vertex isn&#39;t included in the definition of an internal vertex as a BST with only one vertex (that root vertex) could technically fit the definition of a leaf as well.</p><br><p>In the illustrated example, vertex 15 is the root, vertices 5, 7, and 50 are the leaves, and vertices 4, 6, 15 (which is also the root), 23, and 71 are the internal vertices.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="3-10" title='Go to the previous slide 3-10'>&larr;</div>

  <div class='electure-next' data-nextid="4-1" title='Go to the next slide 4-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-4-1" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Each vertex has several key attributes: pointer to the left child, pointer to the right child, pointer to the parent vertex, key/value/data, and special for this visualization that implements &#39;multiset&#39;: frequency of each key (there are potential other attributes). Not all attributes will be used for all vertices, e.g., the leaf vertex will have both their left and right child attributes = NULL. Some other implementation separates key (for ordering of vertices in the BST) with the actual <i>satellite data</i> associated with the keys.</p><br><p>The left/right child of a vertex (except leaf) is drawn on the left/right and below of that vertex, respectively. The parent of a vertex (except root) is drawn above that vertex. The (integer) key of each vertex is drawn inside the circle that represent that vertex and if there are duplicated insertion of the same (integer) key, there will be an additional hyphen &#39;-&#39; and the actual frequency (≥ 2) of that key. In the example above, (key) 15 has 6 as its left child and 23 as its right child. Thus the parent of 6 (and 23) is 15. Some keys may have &#39;-&#39; (actual frequency) in random fashion.</p><br><p>Discussion: It is actually possible to omit the parent pointer from each vertex. How?</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="4" title='Go to the previous slide 4'>&larr;</div>

  <div class='electure-next' data-nextid="4-2" title='Go to the next slide 4-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-4-2" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="4-1" title='Go to the previous slide 4-1'>&larr;</div>

  <div class='electure-next' data-nextid="4-3" title='Go to the next slide 4-3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-4-3" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We allow duplicate integers in this visualization by keeping the <b>N</b> (integer) keys distinct, but any duplication of an existing key will be stored as &#39;frequency&#39; attribute of that key (visualized as &#39;-&#39; (actual frequency, but only if it is &ge; 2)). Thus we can use the simple BST property as follow: For every vertex X, all vertices on the left subtree of X are <b>strictly</b> smaller than X and all vertices on the right subtree of X are <b>strictly</b> greater than X.</p><br><p>In the example above, the vertices on the left subtree of the root 15: {4, 5, 6, 7} are all smaller than 15 and the vertices on the right subtree of the root 15: {23, 50, 71} are all greater than 15. You can recursively check BST property on other vertices too.</p><br><p>In this visualization, we allow the keys to be in range of [-99..99].</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="4-2" title='Go to the previous slide 4-2'>&larr;</div>

  <div class='electure-next' data-nextid="5" title='Go to the next slide 5'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-5" class="electure-dialog" style="bottom:300px;left:60px;width:500px;">
  <p>We provide visualization for the following common BST/AVL Tree operations:</p><ol><li>Query operations (the BST structure remains unchanged):<ol><li>Search(v) (or LowerBound(v)),</li><li>Predecessor(v) (and similarly Successor(v)), and</li><li>Inorder/Preorder/Postorder Traversal,</li></ol></li><li>Update operations (the BST structure (most likely) change):<ol><li>Create BST (several criteria),</li><li>Insert(v), and</li><li>Remove(v).</li></ol></li></ol>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="4-3" title='Go to the previous slide 4-3'>&larr;</div>

  <div class='electure-next' data-nextid="5-1" title='Go to the next slide 5-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-5-1" class="electure-dialog" style="bottom:300px;left:60px;width:500px;">
  <p>There are a few other BST (Query) operations that have not been visualized in VisuAlgo:</p><ol><li>Rank(v): Given a key <b>v</b>, determine what is its rank (1-based index) in the sorted order of the BST elements. That is, Rank(FindMin()) = 1 and Rank(FindMax()) = <b>N</b>. If <b>v</b> does not exist, we can report -1.</li><li>Select(k): Given a rank <b>k</b>, 1 ≤ <b>k</b> ≤ <b>N</b>, determine the key <b>v</b> that has that rank <b>k</b> in the BST. Or in another word, find the <b>k</b>-th smallest element in the BST. That is, Select(1) = FindMin() and Select(<b>N</b>) = FindMax().</li></ol><p>The details of these two operations are currently hidden for pedagogical purpose in a certain NUS course.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="5" title='Go to the previous slide 5'>&larr;</div>

  <div class='electure-next' data-nextid="5-2" title='Go to the next slide 5-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-5-2" class="electure-dialog" style="bottom:300px;left:60px;width:500px;">
  <p>Data structure that is only efficient if there is no (or rare) update, especially the insert and/or remove operation(s) is called <b>static</b> data structure.</p><br><p>Data structure that is efficient even if there are many update operations is called <b>dynamic</b> data structure. BST and especially balanced BST (e.g., AVL Tree) are in this category.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="5-1" title='Go to the previous slide 5-1'>&larr;</div>

  <div class='electure-next' data-nextid="6" title='Go to the next slide 6'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-6" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Because of the way data (distinct integers for this visualization) is organised inside a BST, we can <b>binary</b> search for an integer <b>v</b> efficiently (hence the name of <b>Binary Search</b> Tree).</p><br><p>First, we set the current vertex = root and then check if the current vertex is smaller/equal/larger than integer <b>v</b> that we are searching for. We then go to the right subtree/stop/go the left subtree, respectively. We keep doing this until we either find the required vertex or we don&#39;t.</p><br><p>On the example BST above, try clicking <span class="slide-actions" onclick="doButtonAction2()">Search(23)</span> (found after 2 comparisons), <span class="slide-actions" onclick="doButtonAction1()">Search(7)</span> (found after 3 comparisons), <span class="slide-actions" onclick="doButtonAction3()">Search(21)</span> (not found after 2 comparisons &mdash; at this point we will realize that we cannot find 21).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="5-2" title='Go to the previous slide 5-2'>&larr;</div>

  <div class='electure-next' data-nextid="6-1" title='Go to the next slide 6-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-6-1" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Note that this term is based on the definition given in <a href="https://en.cppreference.com/w/cpp/container/set/lower_bound" target="_blank"><u>C++ std::set::lower_bound</u></a>. Other programming languages, e.g., Java TreeSet has a similar method "higher()".</p><hr><p>If <b>v</b> exists in the BST, then lower_bound(v) is the same as Search(v). But, if <b>v</b> does not exist in the BST, lower_bound(v) will find the smallest value in the BST that is strictly larger than <b>v</b> (unless <b>v</b> &gt; the largest element in the BST). This is the location of this currently non-existent <b>v</b> if it is later inserted into this BST.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="6" title='Go to the previous slide 6'>&larr;</div>

  <div class='electure-next' data-nextid="6-2" title='Go to the next slide 6-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-6-2" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Similarly, because of the way data is organised inside a BST, we can find the minimum/maximum element (an integer in this visualization) by starting from root and keep going to the left/right subtree, respectively.</p><br><p>Try clicking <span class="slide-actions" onclick="doButtonAction52()">SearchMin()</span> and <span class="slide-actions" onclick="doButtonAction53()">SearchMax()</span> on the example BST shown above. The answers should be 4 and 71 (both after comparing against 3 integers from root to leftmost vertex/rightmost vertex, respectively).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="6-1" title='Go to the previous slide 6-1'>&larr;</div>

  <div class='electure-next' data-nextid="6-3" title='Go to the next slide 6-3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-6-3" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Search(v)/lower_bound(v)/SearchMin()/SearchMax() operations run in O(<b>h</b>) where <b>h</b> is the height of the BST.</p><br><p>But note that this <b>h</b> can be as tall as O(<b>N</b>) in a normal BST as shown in the random &#39;skewed right&#39; example above. Try <span class="slide-actions" onclick="doButtonAction5()">Search(100)</span> (this value should not exist as we only use random integers between [1..99] to generate this random BST and thus the Search routine should check all the way from root to the only leaf in O(<b>N</b>) time &mdash; not efficient.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="6-2" title='Go to the previous slide 6-2'>&larr;</div>

  <div class='electure-next' data-nextid="7" title='Go to the next slide 7'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-7" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Because of the BST properties, we can find the Successor of an integer <b>v</b> (assume that we already know where integer <b>v</b> is located from earlier call of Search(<b>v</b>)) as follows:</p><ol><li>If <b>v</b> has a right subtree, the minimum integer in the right subtree of <b>v</b> must be the successor of <b>v</b>. Try <span class="slide-actions" onclick="doButtonAction6()">Successor(23)</span> (should be 50).</li><li>If <b>v</b> does not have a right subtree, we need to traverse the ancestor(s) of <b>v</b> until we find &#39;a right turn&#39; to vertex <b>w</b> (or alternatively, until we find the first vertex <b>w</b> that is greater than vertex <b>v</b>). Once we find vertex <b>w</b>, we will see that vertex <b>v</b> is the maximum element in the left subtree of <b>w</b>. Try <span class="slide-actions" onclick="doButtonAction54()">Successor(7)</span> (should be 15).</li><li>If <b>v</b> is the maximum integer in the BST, <b>v</b> does not have a successor. Try <span class="slide-actions" onclick="doButtonAction55()">Successor(71)</span> (should be none).</li></ol>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="6-3" title='Go to the previous slide 6-3'>&larr;</div>

  <div class='electure-next' data-nextid="7-1" title='Go to the next slide 7-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-7-1" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>The operations for Predecessor of an integer <b>v</b> are defined similarly (just the mirror of Successor operations).</p><br><p>Try the same three corner cases (but mirrored): <span class="slide-actions" onclick="doButtonAction56()">Predecessor(6)</span> (should be 5), <span class="slide-actions" onclick="doButtonAction57()">Predecessor(50)</span> (should be 23), <span class="slide-actions" onclick="doButtonAction58()">Predecessor(4)</span> (should be none).</p><br><p>At this point, stop and ponder these three Successor(v)/Predecessor(v) cases to ensure that you understand these concepts.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="7" title='Go to the previous slide 7'>&larr;</div>

  <div class='electure-next' data-nextid="7-2" title='Go to the next slide 7-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-7-2" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Predecessor(v) and Successor(v) operations run in O(<b>h</b>) where <b>h</b> is the height of the BST.</p><br><p>But recall that this <b>h</b> can be as tall as O(<b>N</b>) in a normal BST as shown in the random &#39;skewed right&#39; example above. If we call <span class="slide-actions" onclick="doButtonAction64()">Successor(FindMax())</span>, we will go up from that last leaf back to the root in O(<b>N</b>) time &mdash; not efficient.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="7-1" title='Go to the previous slide 7-1'>&larr;</div>

  <div class='electure-next' data-nextid="8" title='Go to the next slide 8'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-8" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We can perform an <b>Inorder Traversal</b> of this BST to obtain a list of sorted integers inside this BST (in fact, if we &#39;flatten&#39; the BST into one line, we will see that the vertices are ordered from smallest/leftmost to largest/rightmost).</p><br><p>Inorder Traversal is a recursive method whereby we visit the left subtree first, exhausts all items in the left subtree, visit the current root, before exploring the right subtree and all items in the right subtree. Without further ado, let&#39;s try <span class="slide-actions" onclick="doButtonAction59()">Inorder Traversal</span> to see it in action on the example BST above.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="7-2" title='Go to the previous slide 7-2'>&larr;</div>

  <div class='electure-next' data-nextid="8-1" title='Go to the next slide 8-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-8-1" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Inorder Traversal runs in O(<b>N</b>), regardless of the height of the BST.</p><br><p>Discussion: Why?</p><br><p>PS: Some people call insertion of <b>N</b> unordered integers into a BST in O(<b>N</b> log <b>N</b>) and then performing the O(<b>N</b>) Inorder Traversal as &#39;<b>BST sort</b>&#39;. It is rarely used though as there are several easier-to-use (comparison-based) <a href="./sorting"><u>sorting algorithms</u></a> than this.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="8" title='Go to the previous slide 8'>&larr;</div>

  <div class='electure-next' data-nextid="8-2" title='Go to the next slide 8-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-8-2" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="8-1" title='Go to the previous slide 8-1'>&larr;</div>

  <div class='electure-next' data-nextid="8-3" title='Go to the next slide 8-3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-8-3" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We have included the animation for both Preorder and Postorder tree traversal methods.</p><br><p>Basically, in Preorder Traversal, we visit the current root before going to left subtree and then right subtree. For the example BST shown in the background, we have: {{15}, {6, 4, 5, 7}, {23, 71, 50}}. PS: Do you notice the recursive pattern? root, members of left subtree of root, members of right subtree of root.</p><br><p>In Postorder Traversal, we visit the left subtree and right subtree first, before visiting the current root. For the example BST shown in the background, we have: {{5, 4, 7, 6}, {50, 71, 23}, {15}}.</p><br><p>Discussion: Given a Preorder Traversal of a BST, e.g., [15, 6, 4, 5, 7, 23, 71, 50], can you use it to recover the original BST? Similar question for Postorder is also possible.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="8-2" title='Go to the previous slide 8-2'>&larr;</div>

  <div class='electure-next' data-nextid="8-4" title='Go to the next slide 8-4'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-8-4" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="8-3" title='Go to the previous slide 8-3'>&larr;</div>

  <div class='electure-next' data-nextid="9" title='Go to the next slide 9'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-9" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We can insert a new integer into BST by doing similar operation as <b>Search(v)</b>. But this time, instead of reporting that the new integer is not found, we create a new vertex in the insertion point and put the new integer there. Try <span class="slide-actions" onclick="doButtonAction60()">Insert(60)</span> on the example above (the first insertion will create a new vertex, but see below).</p><br><p>Since we now implement &#39;multiset&#39;, we can insert a duplicate element, e.g., try <span class="slide-actions" onclick="doButtonAction147()">Insert(7)</span> on the example above (multiple times) or click <span class="slide-actions" onclick="doButtonAction60()">Insert(60)</span> again (the duplicate(s)).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="8-4" title='Go to the previous slide 8-4'>&larr;</div>

  <div class='electure-next' data-nextid="9-1" title='Go to the next slide 9-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-9-1" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p><b>Insert(v)</b> runs in O(<b>h</b>) where <b>h</b> is the height of the BST.</p><br><p>By now you should be aware that this <b>h</b> can be as tall as O(<b>N</b>) in a normal BST as shown in the random &#39;skewed right&#39; example above. If we call <span class="slide-actions" onclick="doButtonAction65()">Insert(FindMax()+1)</span>, i.e. we insert a new integer greater than the current max, we will go from root down to the last leaf and then insert the new integer as the right child of that last leaf in O(<b>N</b>) time — not efficient (note that we only allow up to h=9 in this visualization).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="9" title='Go to the previous slide 9'>&larr;</div>

  <div class='electure-next' data-nextid="9-2" title='Go to the next slide 9-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-9-2" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <input class="mcq-answer" id="mcq-answer-20" value="88" hidden><p>Quiz: <b>Inserting integers [1,10,2,9,3,8,4,7,5,6] one by one in that order into an initially empty BST will result in a BST of height:</b></p><form><input type="radio" name="mcq-20-choice" value="90"> The height cannot be determined<br><input type="radio" name="mcq-20-choice" value="87"> 10<br><input type="radio" name="mcq-20-choice" value="89"> 8<br><input type="radio" name="mcq-20-choice" value="88"> 9<br></form><button class="mcq-submit" id="submit-20">Submit</button> <span id="answer-status-20"></span><br><br><p>Pro-tip: You can use the &#39;Exploration mode&#39; to verify the answer.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="9-1" title='Go to the previous slide 9-1'>&larr;</div>

  <div class='electure-next' data-nextid="10" title='Go to the next slide 10'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-10" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We can remove an integer in BST by performing similar operation as <b>Search(v)</b>.</p><br><p>If <b>v</b> is not found in the BST, we simply do nothing.</p><br><p>If <b>v</b> is found in the BST, we do not report that the existing integer <b>v</b> is found, but instead, we do the following checks. If the frequency of <b>v</b> is &ge; 2, we simply decrease its frequency by one without doing anything else. However, if the frequency of <b>v</b> is exactly 1, we perform one of the three possible removal cases that will be elaborated in three separate slides (we suggest that you try each of them one by one).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="9-2" title='Go to the previous slide 9-2'>&larr;</div>

  <div class='electure-next' data-nextid="10-1" title='Go to the next slide 10-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-10-1" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>The first case is the easiest: Vertex <b>v</b> is currently one of the leaf vertex of the BST.</p><br><p>Deletion of a leaf vertex is very easy: We just remove that leaf vertex &mdash; try <span class="slide-actions" onclick="doButtonAction61()">Remove(5)</span> on the example BST above (if the randomization causes vertex 5 to have more than one copy, just click that button again).</p><br><p>This part is clearly O(<b>1</b>) &mdash; on top of the earlier O(<b>h</b>) search-like effort.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="10" title='Go to the previous slide 10'>&larr;</div>

  <div class='electure-next' data-nextid="10-2" title='Go to the next slide 10-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-10-2" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>The second case is also not that hard: Vertex <b>v</b> is an (internal/root) vertex of the BST and it has <b>exactly one child</b>. Removing <b>v</b> without doing anything else will disconnect the BST.</p><br><p>Deletion of a vertex with one child is not that hard: We connect that vertex&#39;s only child with that vertex&#39;s parent &mdash; try <span class="slide-actions" onclick="doButtonAction62()">Remove(23)</span> on the example BST above (if the randomization causes vertex 23 to have more than one copy, just click that button again).</p><br><p>This part is also clearly O(<b>1</b>) &mdash; on top of the earlier O(<b>h</b>) search-like effort.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="10-1" title='Go to the previous slide 10-1'>&larr;</div>

  <div class='electure-next' data-nextid="10-3" title='Go to the next slide 10-3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-10-3" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>The third case is the most complex among the three: Vertex <b>v</b> is an (internal/root) vertex of the BST and it has <b>exactly two children</b>. Removing <b>v</b> without doing anything else will disconnect the BST.</p><br><p>Deletion of a vertex with two children is as follow: We replace that vertex with its successor, and then delete its duplicated successor in its right subtree &mdash; try <span class="slide-actions" onclick="doButtonAction63()">Remove(6)</span> on the example BST above (if the randomization causes vertex 6 to have more than one copy, just click that button again).</p><br><p>This part requires O(<b>h</b>) due to the need to find the successor vertex &mdash; on top of the earlier O(<b>h</b>) search-like effort.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="10-2" title='Go to the previous slide 10-2'>&larr;</div>

  <div class='electure-next' data-nextid="10-4" title='Go to the next slide 10-4'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-10-4" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>This case 3 warrants further discussions:</p><ol><li>Why replacing a vertex <b>B</b> that has two children with its successor <b>C</b> is always a valid strategy?</li><li>Can we replace vertex <b>B</b> that has two children with its predecessor <b>A</b> instead? Why or why not?</li></ol>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="10-3" title='Go to the previous slide 10-3'>&larr;</div>

  <div class='electure-next' data-nextid="10-5" title='Go to the next slide 10-5'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-10-5" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="10-4" title='Go to the previous slide 10-4'>&larr;</div>

  <div class='electure-next' data-nextid="10-6" title='Go to the next slide 10-6'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-10-6" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p><b>Remove(v)</b> runs in O(<b>h</b>) where <b>h</b> is the height of the BST. Removal case 3 (deletion of a vertex with two children is the &#39;heaviest&#39; but it is not more than O(<b>h</b>)).</p><br><p>As you should have fully understand by now, <b>h</b> can be as tall as O(<b>N</b>) in a normal BST as shown in the random &#39;skewed right&#39; example above. If we call <span class="slide-actions" onclick="doButtonAction66()">Remove(FindMax())</span>, i.e. we remove the current max integer, we will go from root down to the last leaf in O(<b>N</b>) time before removing it (when its frequency is 1) &mdash; not efficient.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="10-5" title='Go to the previous slide 10-5'>&larr;</div>

  <div class='electure-next' data-nextid="11" title='Go to the next slide 11'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-11" class="electure-dialog" style="bottom:300px;left:60px;width:500px;">
  <p>To make life easier in &#39;Exploration Mode&#39;, you can create a new BST using these options:</p><ol><li><b>Empty</b> BST (you can then insert a few integers one by one),</li><li>A few <b>e-Lecture Examples</b> that you may have seen several times so far,</li><li><b>Random</b> BST (which is unlikely to be extremely tall &mdash; the expected height of a randomly built BST is still O(log <b>N</b>)),</li><li><b>Skewed Left/Right</b> BST (tall BST with <b>N</b> vertices and <b>N-1</b> linked-list like edges, to showcase the worst case behavior of BST operations; disabled in AVL Tree mode).</li></ol>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="10-6" title='Go to the previous slide 10-6'>&larr;</div>

  <div class='electure-next' data-nextid="12" title='Go to the next slide 12'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-12" class="electure-dialog" style="top:150px;right:60px;width:500px;">
  <p>We are midway through the explanation of this BST module. So far we notice that many basic Table ADT operations run in O(<b>h</b>) and <b>h</b> can be as tall as <b>N-1</b> edges like the &#39;skewed left&#39; example shown — inefficient :(...</p><br><p>So, is there a way to make our BSTs &#39;not that tall&#39;?</p><hr><p>PS: If you want to study how these basic BST operations are implemented in a real program, you can download this <a href="https://www.comp.nus.edu.sg/~stevenha/cs2040/demos/BSTDemo.cpp" target="_blank"><u>BSTDemo.cpp</u></a> | <a href="https://www.comp.nus.edu.sg/~stevenha/cs2040/demos/BSTDemo.py" target="_blank"><u>py</u></a> | <a href="https://www.comp.nus.edu.sg/~stevenha/cs2040/demos/BSTDemo.java" target="_blank"><u>java</u></a>.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="11" title='Go to the previous slide 11'>&larr;</div>

  <div class='electure-next' data-nextid="12-1" title='Go to the next slide 12-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-12-1" class="electure-dialog" style="top:150px;right:60px;width:500px;">
  <p>At this point, we encourage you to press [Esc] or click the X button on the bottom right of this e-Lecture slide to enter the &#39;Exploration Mode&#39; and try various BST operations yourself to strengthen your understanding about this versatile data structure.</p><br><p>When you are ready to continue with the explanation of <b>balanced</b> BST (we use <b>AVL Tree</b> as our example), press [Esc] again or switch the mode back to &#39;e-Lecture Mode&#39; from the top-right corner drop down menu. Then, use the slide selector drop down list to resume from <a href="./bst?slide=12-1"><u>this slide 12-1</u></a>.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="12" title='Go to the previous slide 12'>&larr;</div>

  <div class='electure-next' data-nextid="13" title='Go to the next slide 13'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>We have seen from earlier slides that most of our BST operations except Inorder traversal runs in O(<b>h</b>) where <b>h</b> is the height of the BST that can be as tall as <b>N-1</b>.</p><br><p>We will continue our discussion with the concept of <b>balanced BST</b> so that <b>h</b> = O(log <b>N</b>).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="12-1" title='Go to the previous slide 12-1'>&larr;</div>

  <div class='electure-next' data-nextid="13-1" title='Go to the next slide 13-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-1" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>There are several known implementations of balanced BST, too many to be visualized and explained one by one in VisuAlgo.</p><br><p>We focus on <b>AVL Tree</b> (Adelson-Velskii & Landis, 1962) that is named after its inventor: Adelson-Velskii and Landis.</p><br><p>Other balanced BST implementations (more or less as good or slightly better in terms of constant-factor performance) are: Red-Black Tree, B-trees/2-3-4 Tree (Bayer & McCreight, 1972), Splay Tree (Sleator and Tarjan, 1985), Skip Lists (Pugh, 1989), Treaps (Seidel and Aragon, 1996), etc.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13" title='Go to the previous slide 13'>&larr;</div>

  <div class='electure-next' data-nextid="13-2" title='Go to the next slide 13-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-2" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>To facilitate AVL Tree implementation, we need to <b>augment</b> &mdash; add more information/attribute to &mdash; each BST vertex.</p><br><p>For each vertex <b>v</b>, we define <b>height(v)</b>: The number of edges on the path from vertex <b>v</b> down to its deepest leaf. This attribute is saved in each vertex so we can access a vertex&#39;s height in O(<b>1</b>) without having to recompute it every time.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-1" title='Go to the previous slide 13-1'>&larr;</div>

  <div class='electure-next' data-nextid="13-3" title='Go to the next slide 13-3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-3" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Formally:</p><pre>v.height = -1 (if v is an empty tree)<br>v.height = max(v.left.height, v.right.height) + 1 (otherwise)</pre>The height of the BST is thus: <samp>root.height</samp>.<p></p><br><p>On the example BST above, height(11) = height(32) = height(50) = height(72) = height(99) = 0 (all are leaves). height(29) = 1 as there is 1 edge connecting it to its only leaf 32.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-2" title='Go to the previous slide 13-2'>&larr;</div>

  <div class='electure-next' data-nextid="13-4" title='Go to the next slide 13-4'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-4" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <input class="msq-answer" id="msq-answer-18" value="73,75,77" hidden><p>Quiz: <b>What are the values of height(20), height(65), and height(41) on the BST above?</b></p><input type="checkbox" class="msq-choice" id="msq-18-choice-76"> height(65) = 3<br><input type="checkbox" class="msq-choice" id="msq-18-choice-74"> height(41) = 4<br><input type="checkbox" class="msq-choice" id="msq-18-choice-75"> height(65) = 2<br><input type="checkbox" class="msq-choice" id="msq-18-choice-73"> height(41) = 3<br><input type="checkbox" class="msq-choice" id="msq-18-choice-78"> height(20) = 3<br><input type="checkbox" class="msq-choice" id="msq-18-choice-77"> height(20) = 2<br><button class="msq-submit" id="submit-18">Submit</button> <span id="answer-status-18"></span>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-3" title='Go to the previous slide 13-3'>&larr;</div>

  <div class='electure-next' data-nextid="13-5" title='Go to the next slide 13-5'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-5" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>If we have <b>N</b> elements/items/keys in our BST, the lower bound height <b>h</b> = &Omega;(log<sub>2</sub> <b>N</b>) (the detailed formula in the next slide) if we can somehow insert the <b>N</b> elements in perfect order so that the BST is perfectly balanced.</p><br><p>See the example shown above for <b>N = 15</b> (a perfect BST which is rarely achievable in real life — try inserting any other (distinct) integer and it will not be perfect anymore).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-4" title='Go to the previous slide 13-4'>&larr;</div>

  <div class='electure-next' data-nextid="13-6" title='Go to the next slide 13-6'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-6" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <pre>N ≤ 1 + 2 + 4 + ... + 2<sup>h</sup><br>N ≤ 2<sup>0</sup> + 2<sup>1</sup> + 2<sup>2</sup> + … + 2<sup>h</sup><br>N ≤ 2<sup>h+1</sup>-1 (sum of geometric progression)<br>N+1 ≤ 2<sup>h+1</sup> (apply +1 on both sides)<br>log<sub>2</sub> (N+1) ≤ log<sub>2</sub> 2<sup>h+1</sup> (apply log<sub>2</sub> on both sides)<br>log<sub>2</sub> (N+1) ≤ (h+1) * log<sub>2</sub> 2 (bring down the exponent)<br>log<sub>2</sub> (N+1) ≤ h+1 (log<sub>2</sub> 2 is 1)<br>h+1 ≥ log<sub>2</sub> (N+1) (flip the direction)<br>h ≥ log<sub>2</sub> (N+1)-1 (apply -1 on both sides)<br></pre>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-5" title='Go to the previous slide 13-5'>&larr;</div>

  <div class='electure-next' data-nextid="13-7" title='Go to the next slide 13-7'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-7" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>If we have <b>N</b> elements/items/keys in our BST, the upper bound height <b>h</b> = O(<b>N</b>) if we insert the elements in ascending order (to get skewed right BST as shown above).</p><br><p>The height of such BST is <samp>h = N-1</samp>, so we have <samp>h &lt; N</samp>.</p><br><p>Discussion: Do you know how to get skewed left BST instead?</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-6" title='Go to the previous slide 13-6'>&larr;</div>

  <div class='electure-next' data-nextid="13-8" title='Go to the next slide 13-8'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-8" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-7" title='Go to the previous slide 13-7'>&larr;</div>

  <div class='electure-next' data-nextid="13-9" title='Go to the next slide 13-9'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-13-9" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We have seen that most BST operations are in O(<b>h</b>) and combining the lower and upper bounds of <b>h</b>, we have log<sub>2</sub> <b>N</b> &lt; <b>h</b> &lt; <b>N</b>.</p><br><p>There is a dramatic difference between log<sub>2</sub> <b>N</b> and <b>N</b> and we have seen from the discussion of the lower bound that getting perfect BST (at all times) is near impossible...</p><br><p>So can we have BST that has height closer to log<sub>2</sub> <b>N</b>, i.e. <b>c</b> * log<sub>2</sub> <b>N</b>, for a small constant factor <b>c</b>? If we can, then BST operations that run in O(<b>h</b>) actually run in O(log <b>N</b>)...</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-8" title='Go to the previous slide 13-8'>&larr;</div>

  <div class='electure-next' data-nextid="14" title='Go to the next slide 14'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Introducing AVL Tree, invented by two Russian (Soviet) inventors: Georgy Adelson-Velskii and Evgenii Landis, back in 1962.</p><br><p>In AVL Tree, we will later see that its height <b>h</b> &lt; 2 * log <b>N</b> (tighter analysis exist, but we will use easier analysis in VisuAlgo where <b>c = 2</b>). Therefore, most AVL Tree operations run in O(log <b>N</b>) time &mdash; efficient.</p><br><p>Insert(v) and Remove(v) update operations may change the height <b>h</b> of the AVL Tree, but we will see <b>rotation</b> operation(s) to maintain the AVL Tree height to be low.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="13-9" title='Go to the previous slide 13-9'>&larr;</div>

  <div class='electure-next' data-nextid="14-1" title='Go to the next slide 14-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-1" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>To have efficient performance, we shall not maintain <b>height(v)</b> attribute via the O(<b>N</b>) recursive method every time there is an update (Insert(v)/Remove(v)) operation.</p><br><p>Instead, we compute O(<b>1</b>): <samp>x.height = max(x.left.height, x.right.height) + 1</samp> at the back of our Insert(v)/Remove(v) operation as only the height of vertices along the insertion/removal path may be affected. Thus, only O(<b>h</b>) vertices may change its <b>height(v)</b> attribute and in AVL Tree, <b>h</b> &lt; 2 * log <b>N</b>.</p><br><p>Try <span class="slide-actions" onclick="doButtonAction69()">Insert(37)</span> on the example AVL Tree (ignore the resulting rotation for now, we will come back to it in the next few slides). Notice that only a few vertices along the insertion path: {41,20,29,32} increases their height by +1 and all other vertices will have their heights unchanged.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14" title='Go to the previous slide 14'>&larr;</div>

  <div class='electure-next' data-nextid="14-2" title='Go to the next slide 14-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-2" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Let&#39;s define the following important AVL Tree invariant (property that will never change): A vertex <b>v</b> is said to be <b>height-balanced</b> if <samp>|v.left.height - v.right.height| &le; 1</samp>.</p><br><p>A BST is called height-balanced according to the invariant above if every vertex in the BST is height-balanced. Such BST is called AVL Tree, like the example shown above.</p><br><p>Take a moment to pause here and try inserting a few new random vertices or deleting a few random existing vertices. Will the resulting BST still considered height-balanced?</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-1" title='Go to the previous slide 14-1'>&larr;</div>

  <div class='electure-next' data-nextid="14-3" title='Go to the next slide 14-3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-3" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Adelson-Velskii and Landis claim that an AVL Tree (a height-balanced BST that satisfies AVL Tree invariant) with <b>N</b> vertices has height <b>h</b> &lt; 2 * log<sub>2</sub> <b>N</b>.</p><br><p>The proof relies on the concept of minimum-size AVL Tree of a certain height <b>h</b>.</p><br><p>Let <b>N<sub>h</sub></b> be the minimum number of vertices in a height-balanced AVL Tree of height <b>h</b>.</p><br><p>The first few values of <b>N<sub>h</sub></b> are <b>N<sub>0</sub> = 1</b> (a single root vertex), <b>N<sub>1</sub> = 2</b> (a root vertex with either one left child or one right child only), <b>N<sub>2</sub> = 4</b>, <b>N<sub>3</sub> = 7</b>, <b>N<sub>4</sub> = 12</b>, <b>N<sub>5</sub> = 20</b> (see the background picture), and so on (see the next two slides).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-2" title='Go to the previous slide 14-2'>&larr;</div>

  <div class='electure-next' data-nextid="14-4" title='Go to the next slide 14-4'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-4" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We know that for any other AVL Tree of <b>N</b> vertices (not necessarily the minimum-size one), we have <b>N ≥ N<sub>h</sub></b>.</p><br><img src="https://visualgo.net/img/bst_min_avl1.png" alt="Proof-2"><br><p>In the background picture, we have <b>N<sub>5</sub> = 20</b> vertices but we know that we can squeeze 43 more vertices (up to <b>N = 63</b>) before we have a perfect binary tree of height <b>h = 5</b>.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-3" title='Go to the previous slide 14-3'>&larr;</div>

  <div class='electure-next' data-nextid="14-5" title='Go to the next slide 14-5'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-5" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <pre>N<sub>h</sub> = 1 + N<sub>h-1</sub> + N<sub>h-2</sub> (formula for minimum-size AVL tree of height h)<br>N<sub>h</sub> &gt; 1 + 2*N<sub>h-2</sub> (as N<sub>h-1</sub> > N<sub>h-2</sub>)<br>N<sub>h</sub> &gt; 2*N<sub>h-2</sub> (obviously)<br>N<sub>h</sub> &gt; 4*N<sub>h-4</sub> (recursive)<br>N<sub>h</sub> &gt; 8*N<sub>h-6</sub> (another recursive step)<br>... (we can only do this h/2 times, assuming initial h is even)<br>N<sub>h</sub> &gt; 2<sup>h/2</sup>*N<sub>0</sub> (we reach base case)<br>N<sub>h</sub> &gt; 2<sup>h/2</sup> (as N<sub>0</sub> = 1)</pre><center><img style="width: 70%" src="https://visualgo.net/img/bst_min_avl2.png" alt="Proof-3"></center>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-4" title='Go to the previous slide 14-4'>&larr;</div>

  <div class='electure-next' data-nextid="14-6" title='Go to the next slide 14-6'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-6" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <pre>N &ge; N<sub>h</sub> &gt; 2<sup>h/2</sup> (combining the previous two slides)<br>N &gt; 2<sup>h/2</sup><br>log<sub>2</sub>(N) &gt; log<sub>2</sub>(2<sup>h/2</sup>) (log<sub>2</sub> on both sides)<br>log<sub>2</sub>(N) &gt; h/2 (formula simplification)<br>2 * log<sub>2</sub>(N) &gt; h or h &lt; 2 * log<sub>2</sub>(N)<br>h = O(log(N)) (the final conclusion)</pre><center><img style="width: 30%" src="https://visualgo.net/img/bst_min_avl3.png" alt="Proof-4"></center>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-5" title='Go to the previous slide 14-5'>&larr;</div>

  <div class='electure-next' data-nextid="14-7" title='Go to the next slide 14-7'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-7" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>Look at the example BST again. See that all vertices are height-balanced, an AVL Tree.</p><br><p>To quickly detect if a vertex <b>v</b> is height balanced or not, we modify the AVL Tree invariant (that has absolute function inside) into: <samp>bf(v) = v.left.height - v.right.height</samp>.</p><br><p>Now try <span class="slide-actions" onclick="doButtonAction69()">Insert(37)</span> on the example AVL Tree again. A few vertices along the insertion path: {41,20,29,32} increases their height by +1. Vertices {29,20} will no longer be height-balanced after this insertion (and will be rotated later &mdash; discussed in the next few slides), i.e. bf(29) = -2 and bf(20) = -2 too. We need to restore the balance.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-6" title='Go to the previous slide 14-6'>&larr;</div>

  <div class='electure-next' data-nextid="14-8" title='Go to the next slide 14-8'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-8" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <img src="https://visualgo.net/img/tree_rotation.png" alt="Tree Rotation" width="500"><br><p>See the picture above. Calling <b>rotateRight(D)</b> on the left picture will produce the right picture. Calling <b>rotateLeft(B)</b> on the right picture will produce the left picture again.</p><br><p><b>rotateRight(T)</b>/<b>rotateLeft(T)</b> can only be called if <b>T</b> has a left/right child, respectively.</p><br><p>Tree Rotation <b>preserves</b> BST property.<br>Before rotation, A &lt; B &lt; C &lt; D &lt; E.<br>After rotation, notice that subtree rooted at C (if it exists) changes parent,<br>but the order of A &lt; B &lt; C &lt; D &lt; E does not change.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-7" title='Go to the previous slide 14-7'>&larr;</div>

  <div class='electure-next' data-nextid="14-9" title='Go to the next slide 14-9'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-9" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <pre>BSTVertex rotateLeft(BSTVertex T) // pre-req: T.right != null<br>  BSTVertex w = T.right // rotateRight is the mirror copy of this<br>  w.parent = T.parent // this method is hard to get right for newbie<br>  T.parent = w<br>  T.right = w.left<br>  if (w.left != null) w.left.parent = T<br>  w.left = T<br>  // update the height of T and then w here<br>  return w</pre>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-8" title='Go to the previous slide 14-8'>&larr;</div>

  <div class='electure-next' data-nextid="14-10" title='Go to the next slide 14-10'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-10" class="electure-dialog" style="top:70px;left:50%;margin-left:-250px;width:500px;">
  <img src="https://visualgo.net/img/four_cases.png" alt="Four Cases" width="500"><br><p>There are only these four cases:</p><ol><li>Left Left Case: bf(F) = +2 and bf(D) = +1, solution: rotateRight(F)</li><li>Left Right Case: bf(F) = +2 and bf(B) = -1, solution: rotateLeft(B) first to transform this case into Left Left Case again, then go to step 1</li><li>Right Right Case: bf(B) = -2 and bf(D) = -1, solution: rotateLeft(B)</li><li>Right Left Case: bf(B) = -2 and bf(F) = +1, solution: rotateRight(F) first to transform this case into Right Right Case again, then go to step 3</li></ol>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-9" title='Go to the previous slide 14-9'>&larr;</div>

  <div class='electure-next' data-nextid="14-11" title='Go to the next slide 14-11'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-11" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <ol><li>Just insert <b>v</b> as in normal BST,</li><li>Walk up the AVL Tree from the insertion point back to the root and at every step, we update the height and balance factor of the affected vertices:<ol type="a"><li>Stop at the <b>first</b> vertex that is out-of-balance (+2 or -2), if any,</li><li>Use <b>one</b> of the four tree rotation cases to rebalance it again, e.g. try <span class="slide-actions" onclick="doButtonAction69()">Insert(37)</span> on the example above and notice by calling <b>rotateLeft(29)</b> once, we fix the imbalance issue.</li></ol></li></ol><p>Discussion: Is there other tree rotation cases for Insert(v) operation of AVL Tree?</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-10" title='Go to the previous slide 14-10'>&larr;</div>

  <div class='electure-next' data-nextid="14-12" title='Go to the next slide 14-12'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-12" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-11" title='Go to the previous slide 14-11'>&larr;</div>

  <div class='electure-next' data-nextid="14-13" title='Go to the next slide 14-13'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-13" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <ol><li>Just remove <b>v</b> as in normal BST (one of the three removal cases),</li><li>Walk up the AVL Tree from the deletion point back to the root and at every step, we update the height and balance factor of the affected vertices:<ol><li>Now for <b>every</b> vertex that is out-of-balance (+2 or -2), we use <b>one</b> of the four tree rotation cases to rebalance <b>them</b> (can be more than one) again.</li></ol></li></ol><p>The main difference compared to Insert(v) in AVL tree is that we may trigger one of the four possible rebalancing cases <b>several times</b>, but not more than <b>h</b> = O(log <b>N</b>) times :O, try <span class="slide-actions" onclick="doButtonAction68()">Remove(7)</span> on the example above to see two chain reactions <b>rotateRight(6)</b> and then <b>rotateRight(16)+rotateLeft(8)</b> combo.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-12" title='Go to the previous slide 14-12'>&larr;</div>

  <div class='electure-next' data-nextid="14-14" title='Go to the next slide 14-14'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-14-14" class="electure-dialog" style="top:310px;left:50%;margin-left:-250px;width:500px;">
  <p>We have now see how AVL Tree defines the height-balance invariant, maintain it for all vertices during Insert(v) and Remove(v) update operations, and a proof that AVL Tree has <b>h</b> &lt; 2 * log <b>N</b>.</p><br><p>Therefore, <b>all</b> BST operations (both update and query operations except Inorder Traversal) that we have learned so far, if they have time complexity of O(<b>h</b>), they have time complexity of O(log <b>N</b>) if we use AVL Tree version of BST.</p><br><p>This marks the end of this e-Lecture, but please switch to &#39;Exploration Mode&#39; and try making various calls to Insert(v) and Remove(v) in AVL Tree mode to strengthen your understanding of this data structure.</p><hr><p>PS: If you want to study how these seemingly complex AVL Tree (rotation) operations are implemented in a real program, you can download this <a href="https://github.com/stevenhalim/cpbook-code/blob/master/ch2/nonlineards/AVL.cpp" target="_blank"><u>AVLDemo.cpp</u></a> | <a href="https://github.com/stevenhalim/cpbook-code/blob/master/ch2/nonlineards/AVL.java" target="_blank"><u>java</u></a> (must be used together with this <a href="http://www.comp.nus.edu.sg/~stevenha/cs2040/demos/BSTDemo.cpp" target="_blank"><u>BSTDemo.cpp</u></a> | <a href="http://www.comp.nus.edu.sg/~stevenha/cs2040/demos/BSTDemo.java" target="_blank"><u>java</u></a>).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-13" title='Go to the previous slide 14-13'>&larr;</div>

  <div class='electure-next' data-nextid="15" title='Go to the next slide 15'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-15" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>We will end this module with a few more interesting things about BST and balanced BST (especially AVL Tree).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="14-14" title='Go to the previous slide 14-14'>&larr;</div>

  <div class='electure-next' data-nextid="15-1" title='Go to the next slide 15-1'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-15-1" class="electure-dialog" style="top:70px;left:60px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="15" title='Go to the previous slide 15'>&larr;</div>

  <div class='electure-next' data-nextid="15-2" title='Go to the next slide 15-2'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-15-2" class="electure-dialog" style="top:70px;left:60px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="15-1" title='Go to the previous slide 15-1'>&larr;</div>

  <div class='electure-next' data-nextid="15-3" title='Go to the next slide 15-3'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-15-3" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>For a few more interesting questions about this data structure, please practice on <a href="https://visualgo.net/training?diff=Medium&amp;n=7&amp;tl=0&amp;module=bst,avl"><u>BST/AVL</u></a> training module (no login is required).</p><br><p>However, for registered users, you should login and click the training icon from the homepage to officially clear this module and such achievement will be recorded in your user account.</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="15-2" title='Go to the previous slide 15-2'>&larr;</div>

  <div class='electure-next' data-nextid="15-4" title='Go to the next slide 15-4'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-15-4" class="electure-dialog" style="top:70px;left:60px;width:500px;">
  <p>We also have a few programming problems that somewhat requires the usage of this <b>balanced</b> BST (like AVL Tree) data structure: <a href="https://open.kattis.com/problems/compoundwords" title="" target="_blank"><u>Kattis - compoundwords</u></a> and <a href="https://open.kattis.com/problems/baconeggsandspam" title="" target="_blank"><u>Kattis - baconeggsandspam</u></a>.</p><br><p>Try them to consolidate and improve your understanding about this data structure. You are allowed to use C++ STL map/set, Java TreeMap/TreeSet, or OCaml <a href="https://caml.inria.fr/pub/docs/manual-ocaml/libref/Map.html" target="_blank"><u>Map</u></a>/<a href="https://caml.inria.fr/pub/docs/manual-ocaml/libref/Set.html" target="_blank"><u>Set</u></a> if that simplifies your implementation (Note that Python doesn&#39;t have built-in bBST implementation).</p>

<div class="electure-addition">
</div>

  <div class='electure-prev' data-nextid="15-3" title='Go to the previous slide 15-3'>&larr;</div>

  <div class='electure-next' data-nextid="15-5" title='Go to the next slide 15-5'>&rarr;</div>

  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>
    <div id="electure-15-5" class="electure-dialog" style="top:70px;left:60px;width:500px;">
 
  <div style="background-color: white; color: black;">
  <div class="electure-addition">
    <p>The content of this interesting slide (the answer of the usually intriguing discussion point from the earlier slide) is hidden and only available for legitimate CS lecturer worldwide. This mechanism is used in the various <a href="https://en.wikipedia.org/wiki/Flipped_classroom" target="_blank"><u>flipped classrooms</u></a> in NUS.</p><br>
    <p><b>If you are really a CS lecturer (or an IT teacher)</b> (outside of NUS) and are interested to know the answers, please drop an email to stevenhalim at gmail dot com (<b>show your University staff profile/relevant proof to Steven</b>) for Steven to manually activate this CS lecturer-only feature for you.</p><br>
    <p>FAQ: This feature will <b>NOT</b> be given to anyone else who is not a CS lecturer.</p>
  </div>
  </div>

<div class="electure-addition">
  <hr>
  <p>You have reached the last slide. Return to 'Exploration Mode' to start exploring!</p>
  <p>Note that if you notice any bug in this visualization or if you want to request for a new visualization feature, do not hesitate to drop an email to the project leader: Dr Steven Halim via his email address: stevenhalim at gmail dot com.</p>
</div>

  <div class='electure-prev' data-nextid="15-4" title='Go to the previous slide 15-4'>&larr;</div>


  <div class="electure-read-status" title='Spend some more time reading this slide'>&#128337;</div>
</div>

    <div id="popup" hidden>
      <div id="popup-content"></div>
      <span id="hide-popup" hidden>X <u>Close</u></span>
    </div>

  
    <div id="rotateDeviceOverlay" style="display: none;">
      <div id="rotateDeviceText" style="font-size: 45px; font-weight: bold; text-align: center">Please rotate your device to landscape mode for a better user experience</div>
      <div id="widenDeviceText" style="font-size: 45px; font-weight: bold; text-align: center">Please make the window wider for a better user experience</div>
    </div>
<!--?= console_log($extraCSS); ?-->


    <style>
        .create {
            bottom: 227px
        }
    </style>
    <style>
        .search {
            bottom: 200px
        }
    </style>
    <style>
        .insert {
            bottom: 173px
        }
    </style>
    <style>
        .remove {
            bottom: 146px
        }
    </style>
    <style>
        .predsucc {
            bottom: 119px
        }
    </style>
    <style>
        .select {
            bottom: 92px
        }
    </style>
    <style>
        .traverse {
            bottom: 65px
        }
    </style>

<div id="actions" class="panel">
            <p class="execAction" id="toggle" onClick="bw.toggleLayout()">Toggle BST Layout</p>
                <p id="create">Create</p>
                <p id="search">Search(v)</p>
                <p id="insert">Insert(v)</p>
                <p id="remove">Remove(v)</p>
                <p id="predsucc">Predec-/Succ-essor(v)</p>
                <p id="select">Select(k)</p>
                <p id="traverse">Traverse(root)</p>
    </div>
<div id="actions-hide" class="panel-hide unselectable"><span style="color:white; font-size: x-large; display: inline-block;">&gt;</span></div>
<div id="actions-extras">
    <div class="create action-menu-pullout">
            <div id="create-empty" class="execAction new-menu-option coloured-menu-option" onClick="example(0); openAction(&#039;create&#039;);">
            <p>Empty</p>
            </div>
            <div id="create-example" class="execAction new-menu-option coloured-menu-option" onClick="toggleChildExtras(&#039;create&#039;, &#039;create-example&#039;)">
            <p>Examples</p>
                    <div id="create-example-third-tier" class="create-example-third-tier new-menu-option" style="display: none;">
                            <div id="create-example-min-AVL" class="execAction coloured-menu-option" style="float: right;" onClick="example(5)">
        <p>Min AVL Tree</p>
    </div>
                            <div id="create-example-perfectly-balanced" class="execAction coloured-menu-option" style="float: right;" onClick="example(3)">
        <p>Perfectly Balanced</p>
    </div>
                            <div id="create-example-balanced" class="execAction coloured-menu-option" style="float: right;" onClick="example(2)">
        <p>Balanced</p>
    </div>
                            <div id="create-example-unbalanced" class="execAction coloured-menu-option" style="float: right;" onClick="example(1)">
        <p>Unbalanced</p>
    </div>
                        </div>
            </div>
            <div id="create-random-input" class="new-menu-option">
            N = <input id="N" type="number"  title="Enter an Integer" autocomplete="off" min="1" max="99" value="16" maxlength="2" >                </div>
            <div id="create-random" class="execAction new-menu-option coloured-menu-option" onClick="random(); openAction(&#039;create&#039;);">
            <p>Random</p>
            </div>
            <div id="create-skewed" class="execAction new-menu-option coloured-menu-option" onClick="toggleChildExtras(&#039;create&#039;, &#039;create-skewed&#039;)">
            <p>Skewed</p>
                    <div id="create-skewed-third-tier" class="create-skewed-third-tier new-menu-option" style="display: none;">
                            <div id="create-skewed-right" class="execAction coloured-menu-option" style="float: right;" onClick="skewed(&#039;right&#039;)">
        <p>Right</p>
    </div>
                            <div id="create-skewed-left" class="execAction coloured-menu-option" style="float: right;" onClick="skewed(&#039;left&#039;)">
        <p>Left</p>
    </div>
                        </div>
            </div>
            <div id="create-err" class="err" style="float: left;"></div>
    </div>
    <div class="search action-menu-pullout">
            <div id="search-input" class="new-menu-option">
            v = <input id="v-search" type="number"  title="Enter an Integer" autocomplete="off" min="0" max="99" value="7" >                </div>
            <div id="search-exact" class="execAction new-menu-option coloured-menu-option" onClick="searchVertex(0)">
            <p>Exact</p>
            </div>
            <div id="search-lowerbound" class="execAction new-menu-option coloured-menu-option" onClick="searchVertex(1)">
            <p>lower_bound</p>
            </div>
            <p id="search-plaintext" style="transform: translate(0%, 25%);" class="new-menu-option">
        Extreme:
    </p>
            <div id="search-min" class="execAction new-menu-option coloured-menu-option" onClick="findMinMax(true)">
            <p>Min</p>
            </div>
            <div id="search-max" class="execAction new-menu-option coloured-menu-option" onClick="findMinMax(false)">
            <p>Max</p>
            </div>
            <div id="search-err" class="err" style="float: left;"></div>
    </div>
    <div class="insert action-menu-pullout">
            <div id="insert-input" class="new-menu-option">
            v = <input id="v-insert" type="text"  title="Enter an Integer or comma-separated array of Integers" autocomplete="off" value="1,77" style="width: 200px" >                </div>
            <div id="insert-go" class="execAction new-menu-option coloured-menu-option" onClick="insertVertex()">
            <p>Go</p>
            </div>
            <div id="insert-err" class="err" style="float: left;"></div>
    </div>
    <div class="remove action-menu-pullout">
            <div id="remove-input" class="new-menu-option">
            v = <input id="v-remove" type="text"  title="Enter an Integer or comma-separated array of Integers" autocomplete="off" value="1,77" style="width: 200px" >                </div>
            <div id="remove-go" class="execAction new-menu-option coloured-menu-option" onClick="removeVertex()">
            <p>Go</p>
            </div>
            <div id="remove-err" class="err" style="float: left;"></div>
    </div>
    <div class="predsucc action-menu-pullout">
            <div id="predsucc-input" class="new-menu-option">
            v = <input id="v-predsucc" type="number"  title="Enter an Integer" autocomplete="off" min="0" max="99" value="15" >                </div>
            <div id="predsucc-pred-go" class="execAction new-menu-option coloured-menu-option" onClick="predsucc(true)">
            <p>Get Predecessor</p>
            </div>
            <div id="predsucc-succ-go" class="execAction new-menu-option coloured-menu-option" onClick="predsucc(false)">
            <p>Get Successor</p>
            </div>
            <div id="predsucc-err" class="err" style="float: left;"></div>
    </div>
    <div class="select action-menu-pullout">
            <div id="select-k-input" class="new-menu-option">
            k = <input id="k-select" type="number"  title="Enter an Integer" autocomplete="off" min="1" max="99" value="16" maxlength="2" >                </div>
            <div id="select-go" class="execAction new-menu-option coloured-menu-option" onClick="select()">
            <p>Go</p>
            </div>
            <div id="select-err" class="err" style="float: left;"></div>
    </div>
    <div class="traverse action-menu-pullout">
            <div id="inorder-go" class="execAction new-menu-option coloured-menu-option" onClick="traversal(0)">
            <p>Inorder(root)</p>
            </div>
            <div id="preorder-go" class="execAction new-menu-option coloured-menu-option" onClick="traversal(1)">
            <p>Preorder(root)</p>
            </div>
            <div id="postorder-go" class="execAction new-menu-option coloured-menu-option" onClick="traversal(2)">
            <p>Postorder(root)</p>
            </div>
            <div id="traverse-err" class="err" style="float: left;"></div>
    </div>
</div>
    <!-- Happiness is not something readymade. It comes from your own actions. - Dalai Lama -->

      </div>

<!--  // turned off from 18 Aug 2023
            <div id="gdpr-popup">
        <p>We use cookies to improve our website.<br>By clicking ACCEPT, you agree to our use of Google Analytics for analysing user behaviour and improving user experience as described in our <a id="gdpr-privacy-policy" href="javascript:" style="text-decoration: underline">Privacy Policy</a>.<br>By clicking reject, only cookies necessary for site functions will be used.</p>
        <a id="gdpr-accept" class="gdpr-button">ACCEPT</a>
        <a id="gdpr-reject" class="gdpr-button">REJECT</a>
      </div>
       -->
      <div id="bottom-bar">
      <a id="scale" style="display: none;">1.0x</a>
      <!-- TODO: Make share into a translateable element. -->
      <a id="trigger-share" class="unselectable" style="display: none">Share</a>
      <a id="trigger-about" class="unselectable" >About</a>
      <a id="trigger-team" class="unselectable" >Team</a>
      <a id="trigger-terms" class="unselectable" >Terms of use</a>
      <a id="trigger-privacy" class="unselectable" >Privacy Policy</a>
      <a class="show-if-embed" target="_blank" href=https://visualgo.net/en/bst style="display: none;">Open in Browser</a>
    </div>

    <div id="about" class="overlays">
      <h4>About</h4><span class='close-overlay'>&#x2715;</span>
      <div class='content'>
        <p>Initially conceived in 2011 by Associate Professor Steven Halim, VisuAlgo aimed to facilitate a deeper understanding of data structures and algorithms for his students by providing a self-paced, interactive learning platform.</p><p>Featuring numerous advanced algorithms discussed in Dr. Steven Halim&#39;s book, &#39;Competitive Programming&#39; — co-authored with Dr. Felix Halim and Dr. Suhendry Effendy — VisuAlgo remains the exclusive platform for visualizing and animating several of these complex algorithms even after a decade.</p><p>While primarily designed for National University of Singapore (NUS) students enrolled in various data structure and algorithm courses (e.g., CS1010/equivalent, CS2040/equivalent (including IT5003), CS3230, CS3233, and CS4234), VisuAlgo also serves as a valuable resource for inquisitive minds worldwide, promoting online learning.</p><p>Initially, VisuAlgo was not designed for small touch screens like smartphones, as intricate algorithm visualizations required substantial pixel space and click-and-drag interactions. For an optimal user experience, a minimum screen resolution of 1366x768 is recommended. However, since April 2022, a mobile (lite) version of VisuAlgo has been made available, making it possible to use a subset of VisuAlgo features on smartphone screens.</p><p>VisuAlgo remains a work in progress, with the ongoing development of more complex visualizations. At present, the platform features 24 visualization modules.</p><p>Equipped with a built-in question generator and answer verifier, VisuAlgo&#39;s "online quiz system" enables students to test their knowledge of basic data structures and algorithms. Questions are randomly generated based on specific rules, and students&#39; answers are automatically graded upon submission to our grading server. As more CS instructors adopt this online quiz system worldwide, it could effectively eliminate manual basic data structure and algorithm questions from standard Computer Science exams in many universities. By assigning a small (but non-zero) weight to passing the online quiz, CS instructors can significantly enhance their students&#39; mastery of these basic concepts, as they have access to an almost unlimited number of practice questions that can be instantly verified before taking the online quiz. Each VisuAlgo visualization module now includes its own online quiz component.</p><p>VisuAlgo has been translated into three primary languages: English, Chinese, and Indonesian. Additionally, we have authored public notes about VisuAlgo in various languages, including Indonesian, Korean, Vietnamese, and Thai:</p>
        <a href='https://www.facebook.com/notes/steven-halim/httpidvisualgonet-visualisasi-struktur-data-dan-algoritma-dengan-animasi/10153236934439689' target='_blank'><u>id</u></a>,
        <a href='http://blog.naver.com/visualgo_nus' target='_blank'><u>kr</u></a>,
        <a href='https://www.facebook.com/groups/163215593699283/permalink/824003417620494/' target='_blank'><u>vn</u></a>,
        <a href='http://pantip.com/topic/32736343' target='_blank'><u>th</u></a>.
      </div>
    </div>

    <div id="team" class="overlays">
      <h4>Team</h4><span class='close-overlay'>&#x2715;</span>
      <div class='content'>
        <p>
          <strong><span style='line-height: 150%;'>Project Leader &amp; Advisor (Jul 2011-present)</span></strong><br>
          <a href='https://www.comp.nus.edu.sg/~stevenha/' target='_blank'>Associate Professor Steven Halim</a>,  School of Computing (SoC), National University of Singapore (NUS)<br>
          <a href='https://www.linkedin.com/in/felixhalim/' target='_blank'>Dr Felix Halim</a>, Senior Software Engineer, Google (Mountain View)
        </p>

        <p>
          <strong><span style='line-height: 150%;'>Undergraduate Student Researchers 1</span></strong><br>
          <b>CDTL TEG 1: Jul 2011-Apr 2012</b>: Koh Zi Chun, Victor Loh Bo Huai
        </p>

        <p>
          <strong><span style='line-height: 150%;'>Final Year Project/UROP students 1</span></strong><br>
          <b>Jul 2012-Dec 2013</b>: Phan Thi Quynh Trang, Peter Phandi, Albert Millardo Tjindradinata, Nguyen Hoang Duy<br>
          <b>Jun 2013-Apr 2014</b> <a href='https://www.rosemarietan.com/' target='_blank'>Rose Marie Tan Zhao Yun</a>, Ivan Reinaldo
        </p>

        <p>
          <strong><span style='line-height: 150%;'>Undergraduate Student Researchers 2</span></strong><br>
          <b>CDTL TEG 2: May 2014-Jul 2014</b>: Jonathan Irvin Gunawan, Nathan Azaria, Ian Leow Tze Wei, Nguyen Viet Dung, Nguyen Khac Tung, Steven Kester Yuwono, Cao Shengze, Mohan Jishnu
        </p>

        <p>
          <strong><span style='line-height: 150%;'>Final Year Project/UROP students 2</span></strong><br>
          <b>Jun 2014-Apr 2015</b>: Erin Teo Yi Ling, Wang Zi<br>
          <b>Jun 2016-Dec 2017</b>: Truong Ngoc Khanh, John Kevin Tjahjadi, Gabriella Michelle, Muhammad Rais Fathin Mudzakir<br>
          <b>Aug 2021-Apr 2023</b>: Liu Guangyuan, Manas Vegi, Sha Long, Vuong Hoang Long, Ting Xiao, Lim Dewen Aloysius<br>
        </p>

        <p>
          <strong><span style='line-height: 150%;'>Undergraduate Student Researchers 3</span></strong><br>
          <b>Optiver: Aug 2023-Oct 2023</b>: Bui Hong Duc, Oleh Naver, Tay Ngan Lin<br>
        </p>

        <p>
          <strong><span style='line-height: 150%;'>Final Year Project/UROP students 3</span></strong><br>
          <b>Aug 2023-Apr 2024</b>: Xiong Jingya, Radian Krisno, Ng Wee Han, Tan Chee Heng<br>
          <b>Aug 2024-Apr 2025</b>: Edbert Geraldy Cangdinata, Huang Xing Chen, Nicholas Patrick<br>
        </p>

        <p>
          List of translators who have contributed &ge; 100 translations can be found at <a href="https://visualgo.net/statistics">statistics</a> page.
        </p>

        <p>
          <strong><span style='line-height: 150%;'>Acknowledgements</span></strong><br>
          NUS <a href="https://nus.edu.sg/cdtl" target="_blank"><u>CDTL</u></a> gave Teaching Enhancement Grant to kickstart this project.<div>For Academic Year 2023/24, a generous donation from Optiver will be used to further develop VisuAlgo.</div>
        </p>
      </div>
    </div>

    <div id="termsofuse" class="overlays">
      <h4>Terms of use</h4><span class='close-overlay'>&#x2715;</span>
      <div class='content'>
        <p>VisuAlgo is generously offered at no cost to the global Computer Science community. If you appreciate VisuAlgo, we kindly request that you <b>spread the word about its existence to fellow Computer Science students and instructors</b>. You can share VisuAlgo through social media platforms (e.g., Facebook, YouTube, Instagram, TikTok, Twitter, etc), course webpages, blog reviews, emails, and more.</p><p>Data Structures and Algorithms (DSA) students and instructors are welcome to use this website directly for their classes. If you capture screenshots or videos from this site, feel free to use them elsewhere, provided that you cite the URL of this website (<a href="https://visualgo.net">https://visualgo.net</a>) and/or the list of publications below as references. However, please refrain from downloading VisuAlgo&#39;s client-side files and hosting them on your website, as this constitutes plagiarism. At this time, we do not permit others to fork this project or create VisuAlgo variants. Personal use of an offline copy of the client-side VisuAlgo is acceptable.</p><p>Please note that VisuAlgo&#39;s online quiz component has a substantial server-side element, and it is not easy to save server-side scripts and databases locally. Currently, the general public can access the online quiz system only through the &#39;training mode.&#39; The &#39;test mode&#39; offers a more controlled environment for using randomly generated questions and automatic verification in real examinations at NUS.</p><p><strong><span style="line-height: 200%;">List of Publications</span></strong></p> <p>This work has been presented at the CLI Workshop at the ICPC World Finals 2012 (Poland, Warsaw) and at the IOI Conference at IOI 2012 (Sirmione-Montichiari, Italy). You can click <a href="https://ioinformatics.org/journal/INFOL099.pdf" target="_blank">this link</a> to read our 2012 paper about this system (it was not yet called VisuAlgo back in 2012) and <a href="https://ioinformatics.org/journal/v9_2015_243_245.pdf" target="_blank">this link</a> for the short update in 2015 (to link VisuAlgo name with the previous project).</p><p><strong><span style="line-height: 200%;">Bug Reports or Request for New Features</span></strong></p> <p>VisuAlgo is not a finished project. Associate Professor Steven Halim is still actively improving VisuAlgo. If you are using VisuAlgo and spot a bug in any of our visualization page/online quiz tool or if you want to request for new features, please contact Associate Professor Steven Halim. His contact is the concatenation of his name and add gmail dot com.</p>
      </div>
    </div>

    <div id="privacy-policy" class="overlays">
      <h4>Privacy Policy</h4><span class='close-overlay'>&#x2715;</span>
      <div class='content'>
        <p><b>Version 1.2 (Updated Fri, 18 Aug 2023).</b></p><p>Since Fri, 18 Aug 2023, we no longer use Google Analytics. Thus, all cookies that we use now are solely for the operations of this website. The annoying cookie-consent popup is now turned off even for first-time visitors.</p><p>Since Fri, 07 Jun 2023, thanks to a generous donation by Optiver, anyone in the world can self-create a VisuAlgo account to store a few customization settings (e.g., layout mode, default language, playback speed, etc).</p><p>Additionally, for NUS students, by using a VisuAlgo account (a tuple of NUS official email address, student name as in the class roster, and a password that is encrypted on the server side — no other personal data is stored), you are giving a consent for your course lecturer to keep track of your e-lecture slides reading and online quiz training progresses that is needed to run the course smoothly. Your VisuAlgo account will also be needed for taking NUS official VisuAlgo Online Quizzes and thus passing your account credentials to another person to do the Online Quiz on your behalf constitutes an academic offense. Your user account will be purged after the conclusion of the course unless you choose to keep your account (OPT-IN). Access to the full VisuAlgo database (with encrypted passwords) is limited to Prof Halim himself.</p><p>For other CS lecturers worldwide who have written to Steven, a VisuAlgo account (your (non-NUS) email address, you can use any display name, and encrypted password) is needed to distinguish your online credential versus the rest of the world. Your account will have CS lecturer specific features, namely the ability to see the hidden slides that contain (interesting) answers to the questions presented in the preceding slides before the hidden slides. You can also access Hard setting of the VisuAlgo Online Quizzes. You can freely use the material to enhance your data structures and algorithm classes. Note that there can be other CS lecturer specific features in the future.<br></p><p>For anyone with VisuAlgo account, you can remove your own account by yourself should you wish to no longer be associated with VisuAlgo tool.</p>
      </div>
    </div>
    </div>

    <!-- test replace on 18 Aug 23,, upgrade from 3.6.0 to 3.7.0, see it has issue or not -->
    <!-- <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script> -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js" integrity="sha256-2Pmvv0kuTBOenSvLm6bvfBSSHrUJ+3A7x6P5Ebd07/g=" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/d3-force-boundary@0.0.1/dist/d3-force-boundary.min.js"></script>

    <script>
  $(function () {
    // overlays stuffs
    $('#trigger-about').click(function() {
      if ($(window).width() > 600) {
        $('#dark-overlay').fadeIn(function() {
          $('#about').fadeIn();
        });
      }
      else
        alert('Sorry, this dialog is too big. Please load it on bigger screen');
    });

    $('#trigger-team').click(function() {
      if ($(window).width() > 600) {
        $('#dark-overlay').fadeIn(function() {
          $('#team').fadeIn();
        });
      }
      else
        alert('Sorry, this dialog is too big. Please load it on bigger screen');
    });

    $('#trigger-terms').click(function() {
      if ($(window).width() > 600) {
        $('#dark-overlay').fadeIn(function() {
          $('#termsofuse').fadeIn();
        });
      }
      else
        alert('Sorry, this dialog is too big. Please load it on bigger screen');
    });

    $('#trigger-privacy').click(function () {
      if ($(window).width() > 600) {
        $('#dark-overlay').fadeIn(function() {
          $('#privacy-policy').fadeIn();
        });
      }
      else
        alert('Sorry, this dialog is too big. Please load it on bigger screen');
    })

    $('.close-overlay').click(function() {
      $('.overlays').fadeOut(function() {
        $('#dark-overlay').fadeOut();
      });
    });

    $('#dark-overlay').click(function() {
      $('.overlays').fadeOut();
      $('#dark-overlay').fadeOut();
      if (typeof GeometryWidget !== 'undefined') {
        GeometryWidget.stopLoop();
      }
    });
  })
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-1566631-4"></script>

    <script>
      $.ajaxSetup({
        headers: {
          'X-CSRF-TOKEN': "MZUDnINm1oKaTzu2r7f2ZLMT0JysOZNiPJzL2uIN"
        }
      });

      // handles account dropdown menu
      $(function () {
        $('#language-dropdown-btn').click(function (e) {
          $('#language-dropdown-menu').css('display', 'block');
          $('#account-dropdown-menu').css('display', 'none')
          e.stopPropagation()
        })
        $(document).click(function () {
          $('#language-dropdown-menu').css('display', 'none')
        })
      })

      $(function () {
        $('#account-dropdown-btn').click(function (e) {
          $('#account-dropdown-menu').css('display', 'block')
          $('#language-dropdown-menu').css('display', 'none')
          e.stopPropagation()
        })
        $(document).click(function (e) {
          $('#account-dropdown-menu').css('display', 'none')
        })
      })

      // surprise colour!
      // Referenced to in  home.js and viz.js also
      var colourArray = ["#52bc69", "#d65775"/*"#ed5a7d"*/, "#2ebbd1", "#d9513c", "#fec515", "#4b65ba", "#ff8a27", "#a7d41e"]; // green, pink, blue, red, yellow, indigo, orange, lime

      function disableScroll() { $('html').css('overflow', 'hidden'); }

      function enableScroll() { $('html').css('overflow', 'visible'); }

      function replaceAll(find, replace, str) { return str.replace(new RegExp(find, 'g'), replace); }

      function getColours() {
        var generatedColours = new Array();
        while (generatedColours.length < 4) {
          var n = (Math.floor(Math.random() * colourArray.length));
          if ($.inArray(n, generatedColours) == -1)
            generatedColours.push(n);
        }
        return generatedColours;
      }

      function isOn(value, position) {
        return (value>>position) & 1 === 1;
      }

      // The type can be success, info, warning. Otherwise, we assume it's an error.
      function createAlertBox(msg, type, timeout) {
        // This can be seen in the CSS.
        const animationTimeout = 600;

        if (type !== "info" && type !== "warning" && type !== "success") {
          type = "";
        }

        if (timeout === null || timeout === undefined) {
          timeout = 5000;
        }
        let new_close_button = $('<span class="closebtn unselectable">&times;</span>');
        let new_alert_box = $(`
        <div class="alert ${type}">
          ${msg}
        </div>`).append(new_close_button);
        $("#alert-container").append(new_alert_box);

        let alert_close_handler = () => {
          $(new_alert_box).css("opacity", "0");
          setTimeout(() => new_alert_box.remove(), animationTimeout);
        }

        $(new_close_button).click(alert_close_handler);
        setTimeout(alert_close_handler, timeout);
      }

      function customAlert(msg) {
        $('#custom-alert p').html(msg);
        var m = -1 * ($('#custom-alert').outerHeight()/2);
        $('#custom-alert').css('margin-top', m+'px');
        $('#dark-overlay').fadeIn(function() {
          $('#custom-alert').fadeIn(function() {
            setTimeout(function() {
              $('#custom-alert').fadeOut(function() {
                $('#dark-overlay').fadeOut();
              });
            }, 1000);
          });
        });
      }

      function showLoadingScreen() {
        $('#loading-overlay').show();
        $('#loading-message').show();
      }

      function hideLoadingScreen() {
        $('#loading-overlay').hide();
      }

      function commonAction(retval, msg) {
        if (retval) {
          $('#current-action').show();
          $('#current-action').html(mode == "exploration" ? msg : ("e-Lecture Example (auto play until done)<br>" + msg));
          $('#progress-bar').slider("option", "max", gw.getTotalIteration()-1);
          triggerRightPanels();
          isPlaying = true;
        }
      }

      function getQueryVariable(variable) {
        var query = new URLSearchParams(window.location.search);
        var contents = query.get(variable);
        if (contents === null) {
          return "";
        }
        return contents;
      }

      const MOBILE_WIDTH = 1000;
      const matchMediaMobile = window.matchMedia(`only screen and (max-width: ${MOBILE_WIDTH}px)`);
      const matchMediaNarrow = window.matchMedia(`only screen and (max-width: 500px)`);
      function isMobile() {
        return matchMediaMobile.matches;
      }
      //To fix the issue of a narrow desktop window being asked to rotate, I am now checking for it based on the navigator.userAgent to see if its mobile or not.
      //This may change in the future if browsers decide to change the naming of userAgent for mobile browsers so may need to keep an eye on this.
      function isMobileOS() {
        return /Mobi/i.test(navigator.userAgent) && !/ipad/i.test(navigator.userAgent);
      }
      let portraitMatcher = window.matchMedia("(orientation:portrait)");
      function isPortrait() {
        return portraitMatcher.matches;
      }

      var generatedColours = getColours();
      var surpriseColour = colourArray[generatedColours[0]];
      var colourTheSecond = colourArray[generatedColours[1]];
      var colourTheThird = colourArray[generatedColours[2]];
      var colourTheFourth = colourArray[generatedColours[3]];

      $(function() {
        $('.links').css('background', surpriseColour);
        $('.colour').css("color", surpriseColour);
        $('h4').css("background-color", surpriseColour); // about, contact us etc. button background

        // title
        $('#title a').click(function() {
          $('#title a').removeClass('selected-viz');
          $(this).addClass('selected-viz');
        });
      });

/*
      // GA dropped 26 Jun 2023 and then made official on 18 Aug 2023
/*
      // the sunset-ed GA, commented on 26 Jun 2023, and Prof Halim doesn't bother to use anymore
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
*/

      // function setCookie(cname, cvalue, exdays) {
      //   const d = new Date();
      //   d.setTime(d.getTime() + (exdays*24*60*60*1000));
      //   let expires = "expires="+ d.toUTCString();
      //   document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
      // }

//       //         $(function() {
//           $('#gdpr-accept').click(function () {
// /*
//             // added on 26 Jun 2023
//             window.dataLayer = window.dataLayer || [];
//             function gtag(){dataLayer.push(arguments);}
//             gtag('js', new Date());

//             gtag('config', 'UA-1566631-4');
// */
// //            ga('create', 'UA-1566631-4', 'auto');
// //            ga('send', 'pageview');
//             setCookie('use_google_analytics', 'true', 365)
//             $('#gdpr-popup').hide()
//           });
//           $('#gdpr-reject').click(function () {
//             setCookie('use_google_analytics', 'false', 365)
//             $('#gdpr-popup').hide()
//           });
//         });
//       
      $('#gdpr-privacy-policy').click(function () {
        if ($(window).width() > 600) {
          $('#dark-overlay').fadeIn(function() {
            $('#privacy-policy').fadeIn();
          });
        }
        else
          alert('Sorry, this dialog is too big. Please load it on bigger screen');
      })
    </script>

    <!--<script src="//code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>-->
    <script src="https://visualgo.net/js/jquery-ui.min.js"></script>
    
    <!--<script src="//cdnjs.cloudflare.com/ajax/libs/d3/3.5.16/d3.min.js"></script>-->
    <script src="https://visualgo.net/js/d3.min.js"></script>
    <script src="https://visualgo.net/js/viz-1.0.10.js"></script>
    <!-- Use individual sources for development, minified for deployment-->
    <script src="/js/graph_library/constant.js"></script>
    <script src="/js/graph_library/drawgraph.js"></script>
    <script src="/js/graph_library/misc.js"></script>
    <!-- there's some weird ass dependencies here where GraphWidget relies on properties.js
         This feels damn jank. We should go back to building a minified viz.js rather than
         maintain this jankiness. -->
    <script src="/js/graph_library/properties.js"></script>
    <script src="/js/graph_library/Widget.js"></script>
    <script src="/js/graph_library/GraphTextWidget.js"></script>
    <script src="/js/graph_library/GraphEdgeWidget.js"></script>
    <script src="/js/graph_library/GraphPolygonWidget.js"></script>
    <script src="/js/graph_library/GraphVertexWidget.js"></script>
    <script src="/js/graph_library/GraphWidget.js"></script>
    <script src="/js/graph_library/helperObjects.js?refresh22aug9pm"></script> <!-- Add ?refresh to force update all stalled cached on 22 Aug 2023 after Steven adds a few CS4234 test cases for Steiner Tree, do this properly next time -->
    <script src="/js/graph_library/force_directed_library.js"></script>
    <script src="/js/utils/param_parser.js"></script>
    <!-- <script src="/js/graph_library-1.0.13.js"></script> <!-- turned off on 25 Apr 23 for manual testing -->
    <script>
      let isEmbedded = false;
      // This is checked on load, rather than on the go. Prevents weird behavior
      // like controls not working.
      let isMobileOnLoad = isMobile();

      $(function () {
        let defaultPlaybackSpeed = 1;
                createPlaybackSpeedSlider(defaultPlaybackSpeed);

        $('#scale').show();

        $('#account-dropdown-btn').click(function (e) {
          $('#account-dropdown-menu').css('display', 'block')
          $('#language-dropdown-menu').css('display', 'none')
          e.stopPropagation()
        })
        $(document).click(function (e) {
          $('#account-dropdown-menu').css('display', 'none')
        });
        //Mobile Design Related DOM Manipulations
        if (isMobileOnLoad) {
          $("#status").css({
            "bottom": "10%",
            "height": "12%",
            "max-height": "54px"
          });
          $("#current-action").css("bottom", "22%");
          $('#status-hide').remove();
          $('#left-bar').remove();
          $('#right-bar').remove();
          $("#mode-menu").remove();
          $("#codetrace").css("z-index", 1);
          $("#bottom-bar a").hide();
          $("#bottom-bar").css("height", $("#topbar").css("height"));
          $(".speed-dropup-btn").show();
          $('#scale').show();
          $("#go-to-beginning").remove();
          $("#go-to-end").remove();
          $("#pause").remove();
          $("#play").remove();
          $("#previous").remove();
          $("#next").remove();

          //make progress bar longer
          $("#progress-bar").css({
            left: "25%",
            width: "50%",
            'margin-left': 0
          })
        }

        if (isEmbedded) {
          $("#topbar").hide();
          $("#left-bar").remove();
          $("#right-bar").remove();
          $("#bottom-bar > a").hide();
          $("#status").hide();
          $("#status-hide").hide();
          $("#codetrace").hide();
          $("#codetrace-hide").hide();
          $("#bottom-bar").css("height", $("#topbar").css("height"));
          $("#actions").hide();
          $("#actions-hide").hide();
          $("#viz > svg").width("100%");
          mainSvg.attr("preserveAspectRatio", "xMidYMid meet");

          $(".show-if-embed").show();
          $(".hide-if-embed").hide();
        }
      })

      let mobilePlaybackOverlayTimeout;
      $(function() {
        $("#viz").on("click", () => {
          if (isMobileOnLoad) {
            if ($("#mobile-playback-overlay").is(":hidden") && isPlaying) {
              $("#mobile-playback-overlay").fadeIn();
              hideMobilePlaybackOverlay(6000);
            } else {
              $("#mobile-playback-overlay").fadeOut();
            }
          }
        });
        $("#mobile-playback-overlay").on("click", (event) => {
          if (event.target === event.currentTarget) //to ensure clicks on the controls dont fade the overlay
            $("#mobile-playback-overlay").fadeOut();
          else
            hideMobilePlaybackOverlay(5000);
        })
      });
      function hideMobilePlaybackOverlay(timeOut) {
        if (mobilePlaybackOverlayTimeout)
          clearTimeout(mobilePlaybackOverlayTimeout);
        mobilePlaybackOverlayTimeout = setTimeout(() => {
            $("#mobile-playback-overlay").fadeOut();
        }, timeOut);
      }
      function mobilePlaybackPauseOrPlay() {
        if ($("#mobile-playback-overlay").hasClass("playing")) {
          pause();
          hideMobilePlaybackOverlay(5000);
        } else {
          play();
          hideMobilePlaybackOverlay(3000);
        }
      }
      let rewindLabelTimeout, forwardLabelTimeout;
      function mobilePlaybackRewind() {
        $("#mobile-playback-rewind-label").css("opacity", 1);
        if (rewindLabelTimeout)
          clearTimeout(rewindLabelTimeout);
        rewindLabelTimeout = setTimeout(() => {
          $("#mobile-playback-rewind-label").css("opacity", 0);
        }, 800);
        stepBackward(7);
      }
      function mobilePlaybackForward() {
        $("#mobile-playback-forward-label").css("opacity", 1);
        if (forwardLabelTimeout)
          clearTimeout(forwardLabelTimeout);
        forwardLabelTimeout = setTimeout(() => {
          $("#mobile-playback-forward-label").css("opacity", 0);
        }, 800);
        stepForward(7);
      }

      //let eLectureSessionHistory = {};
      const sectorColors = ['#05a4d0', '#f1c706', '#fa0202'];
      function setSlideTimelineColor(slideNo) {
        const sectionNo = slideNo.split('-')[0];
        $(`[slideNo="${slideNo}"]`).css('background', sectorColors[(parseInt(sectionNo) % 3)]);
      }

      let currSlideTimer = null; //global so that we can clear the timeout when required

      const lectureIds = [{"id":1,"category":"bst","order":1,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 08:11:17","updated_at":"2023-05-26 16:33:27","section":-1,"code":"","section_order":-1,"value":"1","text":"<p>A Binary Search Tree (BST) is a specialized type of binary tree in which each vertex can have up to two children. This structure adheres to the <b>BST property<\/b>, stipulating that every vertex in the left subtree of a given vertex must carry a value smaller than that of the given vertex, and every vertex in the right subtree must carry a value larger. This visualization implements &#39;multiset&#39; property: Although all keys remain distinct integers, information of duplicated integers are stored as a frequency attribute (only shown for keys that appear more than once). For a demonstration, use the <span class=\"slide-actions\" onclick=\"doButtonAction1()\">Search(7)<\/span> function to animate the search for a random value within the range of 1 to 99 in the randomly generated BST above.<\/p><br><p>An Adelson-Velskii Landis (AVL) tree is a <b>self-balancing<\/b> BST that maintains its height within a logarithmic order (O(log <b>N<\/b>)) relative to the number of vertices (<b>N<\/b>) present in the AVL tree.<\/p>","title":"Binary Search Tree"},{"id":2,"category":"bst","order":2,"top":"70px","right":"","bottom":"","left":"280px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 14:21:00","updated_at":"2023-05-18 04:04:50","section":-1,"code":"","section_order":-1,"value":"2","text":"<p>To switch between the standard Binary Search Tree and the AVL Tree (which primarily differs during the insertion and removal of an integer), please select the corresponding header.<\/p><br><p>We also provide a URL shortcut for quick access to the AVL Tree mode, available at <a href=\".\/bst?mode=AVL\"><u>https:\/\/visualgo.net\/en\/avl<\/u><\/a>. The &#39;en&#39; in the URL can be replaced with the two-character code of your preferred language, if available.<\/p>","title":"BST & Balanced BST (AVL Tree)"},{"id":341,"category":"bst","order":3,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-11 03:12:22","updated_at":"2023-06-06 13:06:09","section":-1,"code":"","section_order":-1,"value":"3","text":"<p>A BST, particularly a balanced BST such as an AVL Tree, is an effective data structure for implementing <i>a certain type<\/i> of <b>Table<\/b> (or <b>Map<\/b>) Abstract Data Type (ADT).<\/p><br><p>A Table ADT should efficiently support <b>at least<\/b> the following three operations:<\/p><ol><li>Search(v) \u2014 ascertain whether <b>v<\/b> exists within the ADT,<\/li><li>Insert(v) \u2014 add <b>v<\/b> into the ADT,<\/li><li>Remove(v) \u2014 eliminate <b>v<\/b> from the ADT.<\/li><\/ol><hr><p>For a similar discussion, refer to the <a href=\"https:\/\/visualgo.net\/en\/hashtable?slide=2-1\" target=\"_blank\"><u>Hash Table e-Lecture slides<\/u><\/a>.<\/p>","title":"Motivation"},{"id":377,"category":"bst","order":1,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-16 12:32:58","updated_at":"2023-06-06 13:06:34","section":341,"code":"","section_order":3,"value":"3-1","text":"<p>We are referring to a particular type of Table ADT where the keys must be ordered. This contrasts with other types of Table ADTs that allow for unordered keys.<\/p><br><p>The specific requirements of this Table ADT type will be clarified in the subsequent slides.<\/p>","title":"What Kind of Table ADT?"},{"id":342,"category":"bst","order":2,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-11 09:20:12","updated_at":"2023-05-18 04:13:01","section":341,"code":"","section_order":3,"value":"3-2","text":"<p>Using an <b>unsorted<\/b> array or vector to implement a Table ADT can result in inefficiencies:<\/p><ol><li>Search(v) operates in O(<b>N<\/b>) time complexity because we may need to traverse all <b>N<\/b> elements of the ADT if <b>v<\/b> doesn&#39;t exist,<\/li><li>Insert(v) can be implemented with O(<b>1<\/b>) time complexity, by simply appending <b>v<\/b> at the end of the array,<\/li><li>Remove(v) also runs in O(<b>N<\/b>) time complexity, as we first need to search for <b>v<\/b> (which is already O(<b>N<\/b>)), and then close the gap resulting from the deletion \u2014 also an O(<b>N<\/b>) operation.<\/li><\/ol>","title":"Using Unsorted Array\/Vector"},{"id":343,"category":"bst","order":3,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-11 09:23:56","updated_at":"2023-06-06 13:07:17","section":341,"code":"","section_order":3,"value":"3-3","text":"<p>Implementing a Table ADT with a <b>sorted<\/b> array or vector can enhance the performance of Search(v), but this comes at the expense of Insert(v) performance:<\/p><ol><li>Search(v) can now be implemented with a time complexity of O(log <b>N<\/b>), as we can employ a binary search strategy on the sorted array,<\/li><li>Insert(v) now operates with a time complexity of O(<b>N<\/b>), as we need to use an insertion-sort-like strategy to ensure the array remains sorted,<\/li><li>Remove(v) still runs in O(<b>N<\/b>) time complexity. Although Search(v) operates in O(log <b>N<\/b>), we still have to close the gap resulting from the deletion, which runs in O(<b>N<\/b>).<\/li><\/ol>","title":"Using Sorted Array\/Vector"},{"id":345,"category":"bst","order":4,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-11 09:47:50","updated_at":"2023-05-18 04:32:04","section":341,"code":"const logn_value = document.querySelector(\"#logn\");\nconst n_value = document.querySelector(\"#n\");\nconst input = document.querySelector(\"#logn_input\");\nlogn_value.textContent = input.value;\nn_value.textContent = Math.pow(2, input.value);\ninput.addEventListener(\"input\", (event) => {\n  logn_value.textContent = event.target.value;\n  n_value.textContent = Math.pow(2, event.target.value);\n})","section_order":3,"value":"3-4","text":"<p>The objective of this e-Lecture is to introduce the BST and the balanced BST data structure, namely the AVL Tree, which enable us to implement basic Table ADT operations like Search(v), Insert(v), and Remove(v) \u2014 <b>along with a few other Table ADT operations<\/b> (refer to the next slide) \u2014 in O(log <b>N<\/b>) time. This time complexity is significantly smaller than <b>N<\/b>. Please try the interactive slider below to feel the significant difference.<\/p><br><center><input id=\"logn_input\" type=\"range\" min=\"0\" max=\"40\" value=\"20\"><br><p>log <b>N<\/b> = <output id=\"logn\">20<\/output>, <b>N<\/b> = <output id=\"n\">1048576<\/output>.<\/p><br><\/center><p>PS: More experienced readers may note the existence of <a href=\"hashtable?slide=11-4\"><u>another data structure<\/u><\/a> that can perform these three basic Table ADT operations more swiftly. But, keep reading...<\/p>","title":"O(log N) Complexities?"},{"id":344,"category":"bst","order":5,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-11 09:27:47","updated_at":"2023-06-06 13:07:53","section":341,"code":"","section_order":3,"value":"3-5","text":"<p>In addition to the basic three operations, there are several other Table ADT operations:<\/p><ol><li>Find the Min()\/Max() element,<\/li><li>Find the Successor(v), or the &#39;next larger&#39; element, and Predecessor(v), or the &#39;previous smaller&#39; element,<\/li><li>List elements in sorted order,<\/li><li><a href=\".\/bst?slide=5-1\"><u>Rank(v) & Select(k)<\/u><\/a>,<\/li><li>There are other possible operations as well.<\/li><\/ol><p>Discussion: Given the constraint of using either a sorted or unsorted array\/vector, what would be the optimal implementation for the first three additional operations above?<\/p>","title":"Other Table ADT Operations"},{"id":378,"category":"bst","order":6,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 13:01:14","updated_at":"2023-06-06 13:08:43","section":341,"code":"","section_order":3,"value":"3-6","text":"<p>With an unsorted array, finding the Min()\/Max() operates in O(<b>N<\/b>) time complexity, as we don&#39;t know where the minimum or maximum element is located. Finding the Successor(v)\/Predecessor(v) also runs in O(<b>N<\/b>) for the same reason. Listing elements in sorted order requires using a sorting algorithm, so the time complexity can be O(<b>N<\/b> log <b>N<\/b>).<\/p><br><p>In contrast, with a sorted array, finding the Min()\/Max() operates in O(<b>1<\/b>) time complexity, as the minimum and maximum elements reside in the first and last positions respectively. Finding the Successor(v)\/Predecessor(v) is also O(1) \u2014 simply move back or forward by one index from <b>v<\/b>, respectively. Listing elements in sorted order is a straightforward O(<b>N<\/b>) operation, as it simply involves enumerating from the first to the last element, given that the array is already sorted. This approach appears advantageous, but it becomes ineffective when further insertions and\/or deletions are needed.<\/p>","title":"The Answer"},{"id":349,"category":"bst","order":7,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 08:14:33","updated_at":"2023-05-18 04:37:03","section":341,"code":"","section_order":3,"value":"3-7","text":"<p>The simpler data structure that can be used to implement Table ADT is <a href=\".\/list\"><u>Linked List<\/u><\/a>.<\/p><br><input class=\"mcq-answer\" id=\"mcq-answer-16\" value=\"70\" hidden><p>Quiz: <b>Can we perform all basic three Table ADT operations: Search(v)\/Insert(v)\/Remove(v) efficiently (read: faster than O(<b>N<\/b>)) using Linked List?<\/b><\/p><form><input type=\"radio\" name=\"mcq-16-choice\" value=\"70\"> No<br><input type=\"radio\" name=\"mcq-16-choice\" value=\"69\"> Yes<br><\/form><button class=\"mcq-submit\" id=\"submit-16\">Submit<\/button> <span id=\"answer-status-16\"><\/span><br><br><p>Discussion: Why?<\/p>","title":"What about Linked List?"},{"id":379,"category":"bst","order":8,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 13:05:39","updated_at":"2023-06-06 13:08:10","section":341,"code":"","section_order":3,"value":"3-8","text":"<p>Even when using a <b>sorted<\/b> linked list, executing a binary search isn&#39;t feasible as it&#39;s not easy to instantly jump to the middle element of a linked list. For insertion, an insertion-sort-like process is required to correctly position <b>v<\/b>, which runs in O(<b>N<\/b>) time complexity. Similarly, removal presents the same issue as the search operation.<\/p>","title":"The Answer"},{"id":350,"category":"bst","order":9,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 08:38:28","updated_at":"2023-05-18 04:41:57","section":341,"code":"","section_order":3,"value":"3-9","text":"<p>Another data structure that can be used to implement Table ADT is <a href=\".\/hashtable\"><u>Hash Table<\/u><\/a>. It has very fast Search(v), Insert(v), and Remove(v) performance (all in expected O(<b>1<\/b>) time).<\/p><br><input class=\"mcq-answer\" id=\"mcq-answer-17\" value=\"72\" hidden><p>Quiz: <b>So what is the point of learning this BST module if Hash Table can do the crucial Table ADT operations in unlikely-to-be-beaten expected O(<b>1<\/b>) time?<\/b><\/p><form><input type=\"radio\" name=\"mcq-17-choice\" value=\"71\"> There is no point, so this BST module can be ignored<br><input type=\"radio\" name=\"mcq-17-choice\" value=\"72\"> There are valid reasons, which are ____<br><\/form><button class=\"mcq-submit\" id=\"submit-17\">Submit<\/button> <span id=\"answer-status-17\"><\/span><br><br><p>Discuss the answer above! Hint: Go back to <a href=\".\/bst?slide=3-5\"><u>the previous 4 slides ago<\/u><\/a>.<\/p>","title":"What about Hash Table?"},{"id":380,"category":"bst","order":10,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 13:08:46","updated_at":"2023-06-06 13:09:08","section":341,"code":"","section_order":3,"value":"3-10","text":"<p>Many <a href=\".\/bst?slide=3-5\"><u>additional Table ADT operations<\/u><\/a> require the Table ADT elements to be ordered.<\/p><br><p>If the order of the elements is not a requirement, we can utilize an unordered Hash Table data structure. This structure provides very fast, i.e., O(<b>1<\/b>) time complexity for Search(v), Insert(v), and Remove(v) operations.<\/p><br><p>However, if we need to perform queries that involve the order of elements in the Table ADT, the BST data structure is the preferred choice, particularly its balanced version, which will be discussed shortly.<\/p>","title":"The Answer"},{"id":3,"category":"bst","order":4,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 14:21:30","updated_at":"2023-05-26 17:06:52","section":-1,"code":"$(\"#title-BST\").click();\nexample(1);","section_order":-1,"value":"4","text":"<p>We will now introduce the BST data structure. Refer to the visualization of an example BST provided above!<\/p><br><p>In a BST, the root vertex is unique and has no parent. Conversely, a leaf vertex, of which there can be several, has no children. Vertices that aren&#39;t leaves are known as internal vertices. Occasionally, the root vertex isn&#39;t included in the definition of an internal vertex as a BST with only one vertex (that root vertex) could technically fit the definition of a leaf as well.<\/p><br><p>In the illustrated example, vertex 15 is the root, vertices 5, 7, and 50 are the leaves, and vertices 4, 6, 15 (which is also the root), 23, and 71 are the internal vertices.<\/p>","title":"Visualization"},{"id":334,"category":"bst","order":1,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-09 06:40:30","updated_at":"2025-03-12 05:54:29","section":3,"code":"$(\"#title-BST\").click();\nexample(1);","section_order":4,"value":"4-1","text":"<p>Each vertex has several key attributes: pointer to the left child, pointer to the right child, pointer to the parent vertex, key\/value\/data, and special for this visualization that implements &#39;multiset&#39;: frequency of each key (there are potential other attributes). Not all attributes will be used for all vertices, e.g., the leaf vertex will have both their left and right child attributes = NULL. Some other implementation separates key (for ordering of vertices in the BST) with the actual <i>satellite data<\/i> associated with the keys.<\/p><br><p>The left\/right child of a vertex (except leaf) is drawn on the left\/right and below of that vertex, respectively. The parent of a vertex (except root) is drawn above that vertex. The (integer) key of each vertex is drawn inside the circle that represent that vertex and if there are duplicated insertion of the same (integer) key, there will be an additional hyphen &#39;-&#39; and the actual frequency (\u2265 2) of that key. In the example above, (key) 15 has 6 as its left child and 23 as its right child. Thus the parent of 6 (and 23) is 15. Some keys may have &#39;-&#39; (actual frequency) in random fashion.<\/p><br><p>Discussion: It is actually possible to omit the parent pointer from each vertex. How?<\/p>","title":"BST Vertex Attributes"},{"id":848,"category":"bst","order":2,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2023-05-18 04:52:58","updated_at":"2023-05-26 17:06:39","section":3,"code":"","section_order":4,"value":"4-2","text":"<p>Only the current <a href=\".\/bst?slide=7\"><u>Successor(v) and Predecessor(v) shown in VisuAlgo<\/u><\/a> actually need the parent pointer so that we can go upwards from a vertex to its parent.<\/p><br><p>One day, we will modify the visualization of Successor(v) and Predecessor(v) that search for the Successor\/Predecessor of <b>v<\/b> downwards from the root vertex, thereby removing the need to use the parent pointer, i.e., BST becomes a rooted and directed-downwards only tree.<\/p>","title":"Removing the Parent Pointer"},{"id":337,"category":"bst","order":3,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-09 13:14:52","updated_at":"2023-06-06 13:10:40","section":3,"code":"$(\"#title-BST\").click();\nexample(1);","section_order":4,"value":"4-3","text":"<p>We allow duplicate integers in this visualization by keeping the <b>N<\/b> (integer) keys distinct, but any duplication of an existing key will be stored as &#39;frequency&#39; attribute of that key (visualized as &#39;-&#39; (actual frequency, but only if it is &ge; 2)). Thus we can use the simple BST property as follow: For every vertex X, all vertices on the left subtree of X are <b>strictly<\/b> smaller than X and all vertices on the right subtree of X are <b>strictly<\/b> greater than X.<\/p><br><p>In the example above, the vertices on the left subtree of the root 15: {4, 5, 6, 7} are all smaller than 15 and the vertices on the right subtree of the root 15: {23, 50, 71} are all greater than 15. You can recursively check BST property on other vertices too.<\/p><br><p>In this visualization, we allow the keys to be in range of [-99..99].<\/p>","title":"BST Property"},{"id":335,"category":"bst","order":5,"top":"","right":"","bottom":"300px","left":"60px","marginLeft":"","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-09 06:41:18","updated_at":"2023-11-08 07:57:24","section":-1,"code":"$(\"#search\").addClass(\"menu-highlighted\");\n$(\"#predsucc\").addClass(\"menu-highlighted\");\n$(\"#traverse\").addClass(\"menu-highlighted\");\n$(\"#insert\").addClass(\"menu-highlighted\");\n$(\"#remove\").addClass(\"menu-highlighted\");\n$(\"#create\").addClass(\"menu-highlighted\");","section_order":-1,"value":"5","text":"<p>We provide visualization for the following common BST\/AVL Tree operations:<\/p><ol><li>Query operations (the BST structure remains unchanged):<ol><li>Search(v) (or LowerBound(v)),<\/li><li>Predecessor(v) (and similarly Successor(v)), and<\/li><li>Inorder\/Preorder\/Postorder Traversal,<\/li><\/ol><\/li><li>Update operations (the BST structure (most likely) change):<ol><li>Create BST (several criteria),<\/li><li>Insert(v), and<\/li><li>Remove(v).<\/li><\/ol><\/li><\/ol>","title":"BST Operations"},{"id":383,"category":"bst","order":1,"top":"","right":"","bottom":"300px","left":"60px","marginLeft":"","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-16 13:39:44","updated_at":"2023-11-08 07:57:29","section":335,"code":"","section_order":5,"value":"5-1","text":"<p>There are a few other BST (Query) operations that have not been visualized in VisuAlgo:<\/p><ol><li>Rank(v): Given a key <b>v<\/b>, determine what is its rank (1-based index) in the sorted order of the BST elements. That is, Rank(FindMin()) = 1 and Rank(FindMax()) = <b>N<\/b>. If <b>v<\/b> does not exist, we can report -1.<\/li><li>Select(k): Given a rank <b>k<\/b>, 1 \u2264 <b>k<\/b> \u2264 <b>N<\/b>, determine the key <b>v<\/b> that has that rank <b>k<\/b> in the BST. Or in another word, find the <b>k<\/b>-th smallest element in the BST. That is, Select(1) = FindMin() and Select(<b>N<\/b>) = FindMax().<\/li><\/ol><p>The details of these two operations are currently hidden for pedagogical purpose in a certain NUS course.<\/p>","title":"A Few Other BST Operations"},{"id":351,"category":"bst","order":2,"top":"","right":"","bottom":"300px","left":"60px","marginLeft":"","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 08:50:21","updated_at":"2023-11-08 07:57:29","section":335,"code":"$(\"#insert\").addClass(\"menu-highlighted\");\n$(\"#remove\").addClass(\"menu-highlighted\");","section_order":5,"value":"5-2","text":"<p>Data structure that is only efficient if there is no (or rare) update, especially the insert and\/or remove operation(s) is called <b>static<\/b> data structure.<\/p><br><p>Data structure that is efficient even if there are many update operations is called <b>dynamic<\/b> data structure. BST and especially balanced BST (e.g., AVL Tree) are in this category.<\/p>","title":"Static vs Dynamic Data Structure"},{"id":4,"category":"bst","order":6,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 14:22:02","updated_at":"2023-06-06 13:14:19","section":-1,"code":"$(\"#search\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":-1,"value":"6","text":"<p>Because of the way data (distinct integers for this visualization) is organised inside a BST, we can <b>binary<\/b> search for an integer <b>v<\/b> efficiently (hence the name of <b>Binary Search<\/b> Tree).<\/p><br><p>First, we set the current vertex = root and then check if the current vertex is smaller\/equal\/larger than integer <b>v<\/b> that we are searching for. We then go to the right subtree\/stop\/go the left subtree, respectively. We keep doing this until we either find the required vertex or we don&#39;t.<\/p><br><p>On the example BST above, try clicking <span class=\"slide-actions\" onclick=\"doButtonAction2()\">Search(23)<\/span> (found after 2 comparisons), <span class=\"slide-actions\" onclick=\"doButtonAction1()\">Search(7)<\/span> (found after 3 comparisons), <span class=\"slide-actions\" onclick=\"doButtonAction3()\">Search(21)<\/span> (not found after 2 comparisons &mdash; at this point we will realize that we cannot find 21).<\/p>","title":"Search(v)"},{"id":849,"category":"bst","order":1,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2023-06-06 13:13:56","updated_at":"2023-06-06 13:25:54","section":4,"code":"$(\"#search\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":6,"value":"6-1","text":"<p>Note that this term is based on the definition given in <a href=\"https:\/\/en.cppreference.com\/w\/cpp\/container\/set\/lower_bound\" target=\"_blank\"><u>C++ std::set::lower_bound<\/u><\/a>. Other programming languages, e.g., Java TreeSet has a similar method \"higher()\".<\/p><hr><p>If <b>v<\/b> exists in the BST, then lower_bound(v) is the same as Search(v). But, if <b>v<\/b> does not exist in the BST, lower_bound(v) will find the smallest value in the BST that is strictly larger than <b>v<\/b> (unless <b>v<\/b> &gt; the largest element in the BST). This is the location of this currently non-existent <b>v<\/b> if it is later inserted into this BST.<\/p>","title":"lower_bound(v)"},{"id":336,"category":"bst","order":2,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-09 06:53:18","updated_at":"2023-06-06 13:14:02","section":4,"code":"$(\"#search\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":6,"value":"6-2","text":"<p>Similarly, because of the way data is organised inside a BST, we can find the minimum\/maximum element (an integer in this visualization) by starting from root and keep going to the left\/right subtree, respectively.<\/p><br><p>Try clicking <span class=\"slide-actions\" onclick=\"doButtonAction52()\">SearchMin()<\/span> and <span class=\"slide-actions\" onclick=\"doButtonAction53()\">SearchMax()<\/span> on the example BST shown above. The answers should be 4 and 71 (both after comparing against 3 integers from root to leftmost vertex\/rightmost vertex, respectively).<\/p>","title":"SearchMin() and SearchMax()"},{"id":321,"category":"bst","order":3,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-08 09:28:01","updated_at":"2023-06-06 13:30:05","section":4,"code":"$(\"#search\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nskewed('right');","section_order":6,"value":"6-3","text":"<p>Search(v)\/lower_bound(v)\/SearchMin()\/SearchMax() operations run in O(<b>h<\/b>) where <b>h<\/b> is the height of the BST.<\/p><br><p>But note that this <b>h<\/b> can be as tall as O(<b>N<\/b>) in a normal BST as shown in the random &#39;skewed right&#39; example above. Try <span class=\"slide-actions\" onclick=\"doButtonAction5()\">Search(100)<\/span> (this value should not exist as we only use random integers between [1..99] to generate this random BST and thus the Search routine should check all the way from root to the only leaf in O(<b>N<\/b>) time &mdash; not efficient.<\/p>","title":"O(h) Time Complexity"},{"id":5,"category":"bst","order":7,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 14:23:28","updated_at":"2023-05-26 17:13:19","section":-1,"code":"$(\"#predsucc\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":-1,"value":"7","text":"<p>Because of the BST properties, we can find the Successor of an integer <b>v<\/b> (assume that we already know where integer <b>v<\/b> is located from earlier call of Search(<b>v<\/b>)) as follows:<\/p><ol><li>If <b>v<\/b> has a right subtree, the minimum integer in the right subtree of <b>v<\/b> must be the successor of <b>v<\/b>. Try <span class=\"slide-actions\" onclick=\"doButtonAction6()\">Successor(23)<\/span> (should be 50).<\/li><li>If <b>v<\/b> does not have a right subtree, we need to traverse the ancestor(s) of <b>v<\/b> until we find &#39;a right turn&#39; to vertex <b>w<\/b> (or alternatively, until we find the first vertex <b>w<\/b> that is greater than vertex <b>v<\/b>). Once we find vertex <b>w<\/b>, we will see that vertex <b>v<\/b> is the maximum element in the left subtree of <b>w<\/b>. Try <span class=\"slide-actions\" onclick=\"doButtonAction54()\">Successor(7)<\/span> (should be 15).<\/li><li>If <b>v<\/b> is the maximum integer in the BST, <b>v<\/b> does not have a successor. Try <span class=\"slide-actions\" onclick=\"doButtonAction55()\">Successor(71)<\/span> (should be none).<\/li><\/ol>","title":"Successor(v)"},{"id":338,"category":"bst","order":1,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-09 13:46:17","updated_at":"2023-05-26 17:13:23","section":5,"code":"$(\"#predsucc\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":7,"value":"7-1","text":"<p>The operations for Predecessor of an integer <b>v<\/b> are defined similarly (just the mirror of Successor operations).<\/p><br><p>Try the same three corner cases (but mirrored): <span class=\"slide-actions\" onclick=\"doButtonAction56()\">Predecessor(6)<\/span> (should be 5), <span class=\"slide-actions\" onclick=\"doButtonAction57()\">Predecessor(50)<\/span> (should be 23), <span class=\"slide-actions\" onclick=\"doButtonAction58()\">Predecessor(4)<\/span> (should be none).<\/p><br><p>At this point, stop and ponder these three Successor(v)\/Predecessor(v) cases to ensure that you understand these concepts.<\/p>","title":"Predecessor(v)"},{"id":320,"category":"bst","order":2,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-08 09:26:43","updated_at":"2023-05-26 17:13:25","section":5,"code":"$(\"#predsucc\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nskewed('right');","section_order":7,"value":"7-2","text":"<p>Predecessor(v) and Successor(v) operations run in O(<b>h<\/b>) where <b>h<\/b> is the height of the BST.<\/p><br><p>But recall that this <b>h<\/b> can be as tall as O(<b>N<\/b>) in a normal BST as shown in the random &#39;skewed right&#39; example above. If we call <span class=\"slide-actions\" onclick=\"doButtonAction64()\">Successor(FindMax())<\/span>, we will go up from that last leaf back to the root in O(<b>N<\/b>) time &mdash; not efficient.<\/p>","title":"O(h) Time Complexity"},{"id":6,"category":"bst","order":8,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 14:24:10","updated_at":"2023-06-06 13:35:10","section":-1,"code":"$(\"#traverse\").click().addClass(\"menu-highlighted\");\n$(\"#inorder-go\").addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":-1,"value":"8","text":"<p>We can perform an <b>Inorder Traversal<\/b> of this BST to obtain a list of sorted integers inside this BST (in fact, if we &#39;flatten&#39; the BST into one line, we will see that the vertices are ordered from smallest\/leftmost to largest\/rightmost).<\/p><br><p>Inorder Traversal is a recursive method whereby we visit the left subtree first, exhausts all items in the left subtree, visit the current root, before exploring the right subtree and all items in the right subtree. Without further ado, let&#39;s try <span class=\"slide-actions\" onclick=\"doButtonAction59()\">Inorder Traversal<\/span> to see it in action on the example BST above.<\/p>","title":"Inorder Traversal"},{"id":316,"category":"bst","order":1,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-08 09:18:59","updated_at":"2023-06-06 13:35:14","section":6,"code":"$(\"#traverse\").click().addClass(\"menu-highlighted\");\n$(\"#inorder-go\").addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":8,"value":"8-1","text":"<p>Inorder Traversal runs in O(<b>N<\/b>), regardless of the height of the BST.<\/p><br><p>Discussion: Why?<\/p><br><p>PS: Some people call insertion of <b>N<\/b> unordered integers into a BST in O(<b>N<\/b> log <b>N<\/b>) and then performing the O(<b>N<\/b>) Inorder Traversal as &#39;<b>BST sort<\/b>&#39;. It is rarely used though as there are several easier-to-use (comparison-based) <a href=\".\/sorting\"><u>sorting algorithms<\/u><\/a> than this.<\/p>","title":"O(N) Time Complexity"},{"id":381,"category":"bst","order":2,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 13:15:17","updated_at":"2023-06-06 13:35:18","section":6,"code":"$(\"#traverse\").click().addClass(\"menu-highlighted\");\n$(\"#inorder-go\").addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":8,"value":"8-2","text":"<p>Notice that regardless the structure of the BST, Inorder Traversal will visit each vertex once (to be precise, three times: from parent, returning from left subtree, and returning from right subtree). As there are <b>N<\/b> vertices, Inorder Traversal runs in O(<b>3*N<\/b>) = O(<b>N<\/b>).<\/p>","title":"The Answer"},{"id":425,"category":"bst","order":3,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-18 09:55:35","updated_at":"2023-06-06 13:35:28","section":6,"code":"$(\"#traverse\").click().addClass(\"menu-highlighted\");\n$(\"#preorder-go\").addClass(\"menu-highlighted\");\n$(\"#postorder-go\").addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":8,"value":"8-3","text":"<p>We have included the animation for both Preorder and Postorder tree traversal methods.<\/p><br><p>Basically, in Preorder Traversal, we visit the current root before going to left subtree and then right subtree. For the example BST shown in the background, we have: {{15}, {6, 4, 5, 7}, {23, 71, 50}}. PS: Do you notice the recursive pattern? root, members of left subtree of root, members of right subtree of root.<\/p><br><p>In Postorder Traversal, we visit the left subtree and right subtree first, before visiting the current root. For the example BST shown in the background, we have: {{5, 4, 7, 6}, {50, 71, 23}, {15}}.<\/p><br><p>Discussion: Given a Preorder Traversal of a BST, e.g., [15, 6, 4, 5, 7, 23, 71, 50], can you use it to recover the original BST? Similar question for Postorder is also possible.<\/p>","title":"Preorder and Postorder Traversal"},{"id":850,"category":"bst","order":4,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2023-06-06 13:33:03","updated_at":"2023-06-06 13:39:06","section":6,"code":"$(\"#traverse\").click().addClass(\"menu-highlighted\");\n$(\"#preorder-go\").addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":8,"value":"8-4","text":"<p>If we are given a Preorder Traversal of a BST, e.g., [[15], 6, 4, 5, 7, 23, 71, 50], we know that the <b>first<\/b> element in the Preorder Traversal must be the root of the BST, in this case: 15.<\/p><br><p>We can then scan the rest of the traversal and stop at the first element that is greater than 23, i.e., [6, 4, 5, 7]. This must be the elements of the left subtree of BST rooted at 15. The rest, i.e., [23, 71, 50] must be the elements of the right subtree of BST rooted at 15.<\/p><br><p>We can apply the same recursive process to reconstruct the whole BST.<\/p>","title":"The Answer"},{"id":7,"category":"bst","order":9,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 14:24:36","updated_at":"2023-06-06 13:39:59","section":-1,"code":"$(\"#insert\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":-1,"value":"9","text":"<p>We can insert a new integer into BST by doing similar operation as <b>Search(v)<\/b>. But this time, instead of reporting that the new integer is not found, we create a new vertex in the insertion point and put the new integer there. Try <span class=\"slide-actions\" onclick=\"doButtonAction60()\">Insert(60)<\/span> on the example above (the first insertion will create a new vertex, but see below).<\/p><br><p>Since we now implement &#39;multiset&#39;, we can insert a duplicate element, e.g., try <span class=\"slide-actions\" onclick=\"doButtonAction147()\">Insert(7)<\/span> on the example above (multiple times) or click <span class=\"slide-actions\" onclick=\"doButtonAction60()\">Insert(60)<\/span> again (the duplicate(s)).<\/p>","title":"Insert(v)"},{"id":317,"category":"bst","order":1,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-08 09:23:21","updated_at":"2023-05-26 17:24:23","section":7,"code":"$(\"#insert\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nskewed('right');","section_order":9,"value":"9-1","text":"<p><b>Insert(v)<\/b> runs in O(<b>h<\/b>) where <b>h<\/b> is the height of the BST.<\/p><br><p>By now you should be aware that this <b>h<\/b> can be as tall as O(<b>N<\/b>) in a normal BST as shown in the random &#39;skewed right&#39; example above. If we call <span class=\"slide-actions\" onclick=\"doButtonAction65()\">Insert(FindMax()+1)<\/span>, i.e. we insert a new integer greater than the current max, we will go from root down to the last leaf and then insert the new integer as the right child of that last leaf in O(<b>N<\/b>) time \u2014 not efficient (note that we only allow up to h=9 in this visualization).<\/p>","title":"O(h) Time Complexity"},{"id":360,"category":"bst","order":2,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 01:37:08","updated_at":"2023-05-26 17:30:50","section":7,"code":"","section_order":9,"value":"9-2","text":"<input class=\"mcq-answer\" id=\"mcq-answer-20\" value=\"88\" hidden><p>Quiz: <b>Inserting integers [1,10,2,9,3,8,4,7,5,6] one by one in that order into an initially empty BST will result in a BST of height:<\/b><\/p><form><input type=\"radio\" name=\"mcq-20-choice\" value=\"90\"> The height cannot be determined<br><input type=\"radio\" name=\"mcq-20-choice\" value=\"87\"> 10<br><input type=\"radio\" name=\"mcq-20-choice\" value=\"89\"> 8<br><input type=\"radio\" name=\"mcq-20-choice\" value=\"88\"> 9<br><\/form><button class=\"mcq-submit\" id=\"submit-20\">Submit<\/button> <span id=\"answer-status-20\"><\/span><br><br><p>Pro-tip: You can use the &#39;Exploration mode&#39; to verify the answer.<\/p>","title":"Mini Quiz"},{"id":8,"category":"bst","order":10,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 14:25:01","updated_at":"2023-05-26 17:26:20","section":-1,"code":"$(\"#remove\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":-1,"value":"10","text":"<p>We can remove an integer in BST by performing similar operation as <b>Search(v)<\/b>.<\/p><br><p>If <b>v<\/b> is not found in the BST, we simply do nothing.<\/p><br><p>If <b>v<\/b> is found in the BST, we do not report that the existing integer <b>v<\/b> is found, but instead, we do the following checks. If the frequency of <b>v<\/b> is &ge; 2, we simply decrease its frequency by one without doing anything else. However, if the frequency of <b>v<\/b> is exactly 1, we perform one of the three possible removal cases that will be elaborated in three separate slides (we suggest that you try each of them one by one).<\/p>","title":"Remove(v) - Three Possible Cases"},{"id":346,"category":"bst","order":1,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-11 10:01:18","updated_at":"2023-05-26 17:27:27","section":8,"code":"$(\"#remove\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":10,"value":"10-1","text":"<p>The first case is the easiest: Vertex <b>v<\/b> is currently one of the leaf vertex of the BST.<\/p><br><p>Deletion of a leaf vertex is very easy: We just remove that leaf vertex &mdash; try <span class=\"slide-actions\" onclick=\"doButtonAction61()\">Remove(5)<\/span> on the example BST above (if the randomization causes vertex 5 to have more than one copy, just click that button again).<\/p><br><p>This part is clearly O(<b>1<\/b>) &mdash; on top of the earlier O(<b>h<\/b>) search-like effort.<\/p>","title":"Remove(v) - Case 1"},{"id":339,"category":"bst","order":2,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-09 14:09:47","updated_at":"2023-05-26 17:28:09","section":8,"code":"$(\"#remove\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":10,"value":"10-2","text":"<p>The second case is also not that hard: Vertex <b>v<\/b> is an (internal\/root) vertex of the BST and it has <b>exactly one child<\/b>. Removing <b>v<\/b> without doing anything else will disconnect the BST.<\/p><br><p>Deletion of a vertex with one child is not that hard: We connect that vertex&#39;s only child with that vertex&#39;s parent &mdash; try <span class=\"slide-actions\" onclick=\"doButtonAction62()\">Remove(23)<\/span> on the example BST above (if the randomization causes vertex 23 to have more than one copy, just click that button again).<\/p><br><p>This part is also clearly O(<b>1<\/b>) &mdash; on top of the earlier O(<b>h<\/b>) search-like effort.<\/p>","title":"Remove(v) - Case 2"},{"id":340,"category":"bst","order":3,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-09 14:11:40","updated_at":"2023-05-26 17:28:38","section":8,"code":"$(\"#remove\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":10,"value":"10-3","text":"<p>The third case is the most complex among the three: Vertex <b>v<\/b> is an (internal\/root) vertex of the BST and it has <b>exactly two children<\/b>. Removing <b>v<\/b> without doing anything else will disconnect the BST.<\/p><br><p>Deletion of a vertex with two children is as follow: We replace that vertex with its successor, and then delete its duplicated successor in its right subtree &mdash; try <span class=\"slide-actions\" onclick=\"doButtonAction63()\">Remove(6)<\/span> on the example BST above (if the randomization causes vertex 6 to have more than one copy, just click that button again).<\/p><br><p>This part requires O(<b>h<\/b>) due to the need to find the successor vertex &mdash; on top of the earlier O(<b>h<\/b>) search-like effort.<\/p>","title":"Remove(v) - Case 3"},{"id":347,"category":"bst","order":4,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-11 10:15:17","updated_at":"2023-05-26 17:25:04","section":8,"code":"$(\"#remove\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nexample(1);","section_order":10,"value":"10-4","text":"<p>This case 3 warrants further discussions:<\/p><ol><li>Why replacing a vertex <b>B<\/b> that has two children with its successor <b>C<\/b> is always a valid strategy?<\/li><li>Can we replace vertex <b>B<\/b> that has two children with its predecessor <b>A<\/b> instead? Why or why not?<\/li><\/ol>","title":"Remove(v) - Case 3 Discussion"},{"id":382,"category":"bst","order":5,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 13:18:23","updated_at":"2017-05-16 13:18:43","section":8,"code":"","section_order":10,"value":"10-5","text":"<p>We claim that vertex <b>C<\/b>, which is the successor of vertex <b>B<\/b> that has two children, must only have at most one child (which is an easier removal case).<\/p><br><p>Vertex <b>B<\/b> has two children, so <b>B<\/b> must have a right child. Let&#39;s name it <b>R<\/b>. Successor of <b>B<\/b> must be the minimum vertex of subtree rooted at <b>R<\/b>. Remember that the minimum element of a subtree in BST has <b>no left child<\/b> (it may have right child). Thus, <b>C<\/b>, the successor of <b>B<\/b> has at most one child.<\/p><br><p>Before removal, we have <b>X (may be empty) &lt; A &lt; B &lt; C &lt; Z (may be empty)<\/b> in the BST. Replacing <b>B<\/b> with its successor <b>C<\/b> then deleting the old and duplicate <b>C<\/b> will maintain the BST properties of all vertices involved. Similarly replacing <b>B<\/b> with its predecessor <b>A<\/b> will also achieve the same result. We just need to be consistent.<\/p>","title":"The Answer"},{"id":318,"category":"bst","order":6,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-08 09:24:17","updated_at":"2023-05-26 17:29:28","section":8,"code":"$(\"#remove\").click().addClass(\"menu-highlighted\");\n$(\"#title-BST\").click();\nskewed('right');","section_order":10,"value":"10-6","text":"<p><b>Remove(v)<\/b> runs in O(<b>h<\/b>) where <b>h<\/b> is the height of the BST. Removal case 3 (deletion of a vertex with two children is the &#39;heaviest&#39; but it is not more than O(<b>h<\/b>)).<\/p><br><p>As you should have fully understand by now, <b>h<\/b> can be as tall as O(<b>N<\/b>) in a normal BST as shown in the random &#39;skewed right&#39; example above. If we call <span class=\"slide-actions\" onclick=\"doButtonAction66()\">Remove(FindMax())<\/span>, i.e. we remove the current max integer, we will go from root down to the last leaf in O(<b>N<\/b>) time before removing it (when its frequency is 1) &mdash; not efficient.<\/p>","title":"O(h) Time Complexity"},{"id":9,"category":"bst","order":11,"top":"","right":"","bottom":"300px","left":"60px","marginLeft":"","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2016-11-08 14:25:25","updated_at":"2023-11-08 07:58:51","section":-1,"code":"$(\"#create\").click().addClass(\"menu-highlighted\");","section_order":-1,"value":"11","text":"<p>To make life easier in &#39;Exploration Mode&#39;, you can create a new BST using these options:<\/p><ol><li><b>Empty<\/b> BST (you can then insert a few integers one by one),<\/li><li>A few <b>e-Lecture Examples<\/b> that you may have seen several times so far,<\/li><li><b>Random<\/b> BST (which is unlikely to be extremely tall &mdash; the expected height of a randomly built BST is still O(log <b>N<\/b>)),<\/li><li><b>Skewed Left\/Right<\/b> BST (tall BST with <b>N<\/b> vertices and <b>N-1<\/b> linked-list like edges, to showcase the worst case behavior of BST operations; disabled in AVL Tree mode).<\/li><\/ol>","title":"Create BST"},{"id":348,"category":"bst","order":12,"top":"150px","right":"60px","bottom":"","left":"","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-11 10:23:48","updated_at":"2025-03-12 05:54:38","section":-1,"code":"$(\"#title-BST\").click();\nskewed('left');","section_order":-1,"value":"12","text":"<p>We are midway through the explanation of this BST module. So far we notice that many basic Table ADT operations run in O(<b>h<\/b>) and <b>h<\/b> can be as tall as <b>N-1<\/b> edges like the &#39;skewed left&#39; example shown \u2014 inefficient :(...<\/p><br><p>So, is there a way to make our BSTs &#39;not that tall&#39;?<\/p><hr><p>PS: If you want to study how these basic BST operations are implemented in a real program, you can download this <a href=\"https:\/\/www.comp.nus.edu.sg\/~stevenha\/cs2040\/demos\/BSTDemo.cpp\" target=\"_blank\"><u>BSTDemo.cpp<\/u><\/a> | <a href=\"https:\/\/www.comp.nus.edu.sg\/~stevenha\/cs2040\/demos\/BSTDemo.py\" target=\"_blank\"><u>py<\/u><\/a> | <a href=\"https:\/\/www.comp.nus.edu.sg\/~stevenha\/cs2040\/demos\/BSTDemo.java\" target=\"_blank\"><u>java<\/u><\/a>.<\/p>","title":"Intermezzo"},{"id":353,"category":"bst","order":1,"top":"150px","right":"60px","bottom":"","left":"","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 13:48:35","updated_at":"2023-05-26 17:30:19","section":348,"code":"","section_order":12,"value":"12-1","text":"<p>At this point, we encourage you to press [Esc] or click the X button on the bottom right of this e-Lecture slide to enter the &#39;Exploration Mode&#39; and try various BST operations yourself to strengthen your understanding about this versatile data structure.<\/p><br><p>When you are ready to continue with the explanation of <b>balanced<\/b> BST (we use <b>AVL Tree<\/b> as our example), press [Esc] again or switch the mode back to &#39;e-Lecture Mode&#39; from the top-right corner drop down menu. Then, use the slide selector drop down list to resume from <a href=\".\/bst?slide=12-1\"><u>this slide 12-1<\/u><\/a>.<\/p>","title":"Try Exploration Mode"},{"id":319,"category":"bst","order":13,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-08 09:26:23","updated_at":"2023-05-26 17:31:49","section":-1,"code":"$(\"#title-BST\").click();\nskewed('right');","section_order":-1,"value":"13","text":"<p>We have seen from earlier slides that most of our BST operations except Inorder traversal runs in O(<b>h<\/b>) where <b>h<\/b> is the height of the BST that can be as tall as <b>N-1<\/b>.<\/p><br><p>We will continue our discussion with the concept of <b>balanced BST<\/b> so that <b>h<\/b> = O(log <b>N<\/b>).<\/p>","title":"Balanced BST"},{"id":354,"category":"bst","order":1,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 13:54:07","updated_at":"2023-05-26 17:31:54","section":319,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":13,"value":"13-1","text":"<p>There are several known implementations of balanced BST, too many to be visualized and explained one by one in VisuAlgo.<\/p><br><p>We focus on <b>AVL Tree<\/b> (Adelson-Velskii & Landis, 1962) that is named after its inventor: Adelson-Velskii and Landis.<\/p><br><p>Other balanced BST implementations (more or less as good or slightly better in terms of constant-factor performance) are: Red-Black Tree, B-trees\/2-3-4 Tree (Bayer & McCreight, 1972), Splay Tree (Sleator and Tarjan, 1985), Skip Lists (Pugh, 1989), Treaps (Seidel and Aragon, 1996), etc.<\/p>","title":"AVL Tree"},{"id":355,"category":"bst","order":2,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 13:57:59","updated_at":"2018-03-12 12:30:23","section":319,"code":"","section_order":13,"value":"13-2","text":"<p>To facilitate AVL Tree implementation, we need to <b>augment<\/b> &mdash; add more information\/attribute to &mdash; each BST vertex.<\/p><br><p>For each vertex <b>v<\/b>, we define <b>height(v)<\/b>: The number of edges on the path from vertex <b>v<\/b> down to its deepest leaf. This attribute is saved in each vertex so we can access a vertex&#39;s height in O(<b>1<\/b>) without having to recompute it every time.<\/p>","title":"Extra BST Attribute: height(v)"},{"id":356,"category":"bst","order":3,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 14:10:49","updated_at":"2023-05-26 17:32:48","section":319,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":13,"value":"13-3","text":"<p>Formally:<\/p><pre>v.height = -1 (if v is an empty tree)<br>v.height = max(v.left.height, v.right.height) + 1 (otherwise)<\/pre>The height of the BST is thus: <samp>root.height<\/samp>.<p><\/p><br><p>On the example BST above, height(11) = height(32) = height(50) = height(72) = height(99) = 0 (all are leaves). height(29) = 1 as there is 1 edge connecting it to its only leaf 32.<\/p>","title":"Formal Definition of height(v)"},{"id":357,"category":"bst","order":4,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 14:17:07","updated_at":"2023-05-26 17:32:52","section":319,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":13,"value":"13-4","text":"<input class=\"msq-answer\" id=\"msq-answer-18\" value=\"73,75,77\" hidden><p>Quiz: <b>What are the values of height(20), height(65), and height(41) on the BST above?<\/b><\/p><input type=\"checkbox\" class=\"msq-choice\" id=\"msq-18-choice-76\"> height(65) = 3<br><input type=\"checkbox\" class=\"msq-choice\" id=\"msq-18-choice-74\"> height(41) = 4<br><input type=\"checkbox\" class=\"msq-choice\" id=\"msq-18-choice-75\"> height(65) = 2<br><input type=\"checkbox\" class=\"msq-choice\" id=\"msq-18-choice-73\"> height(41) = 3<br><input type=\"checkbox\" class=\"msq-choice\" id=\"msq-18-choice-78\"> height(20) = 3<br><input type=\"checkbox\" class=\"msq-choice\" id=\"msq-18-choice-77\"> height(20) = 2<br><button class=\"msq-submit\" id=\"submit-18\">Submit<\/button> <span id=\"answer-status-18\"><\/span>","title":"Mini Quiz"},{"id":361,"category":"bst","order":5,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 02:51:37","updated_at":"2023-10-17 07:53:20","section":319,"code":"$(\"#title-AVL\").click();\nexample(3);","section_order":13,"value":"13-5","text":"<p>If we have <b>N<\/b> elements\/items\/keys in our BST, the lower bound height <b>h<\/b> = &Omega;(log<sub>2<\/sub> <b>N<\/b>) (the detailed formula in the next slide) if we can somehow insert the <b>N<\/b> elements in perfect order so that the BST is perfectly balanced.<\/p><br><p>See the example shown above for <b>N = 15<\/b> (a perfect BST which is rarely achievable in real life \u2014 try inserting any other (distinct) integer and it will not be perfect anymore).<\/p>","title":"The Lower Bound of BST Height"},{"id":362,"category":"bst","order":6,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 03:08:51","updated_at":"2023-10-17 07:47:59","section":319,"code":"$(\"#title-AVL\").click();\nexample(3);","section_order":13,"value":"13-6","text":"<pre>N \u2264 1 + 2 + 4 + ... + 2<sup>h<\/sup><br>N \u2264 2<sup>0<\/sup> + 2<sup>1<\/sup> + 2<sup>2<\/sup> + \u2026 + 2<sup>h<\/sup><br>N \u2264 2<sup>h+1<\/sup>-1 (sum of geometric progression)<br>N+1 \u2264 2<sup>h+1<\/sup> (apply +1 on both sides)<br>log<sub>2<\/sub> (N+1) \u2264 log<sub>2<\/sub> 2<sup>h+1<\/sup> (apply log<sub>2<\/sub> on both sides)<br>log<sub>2<\/sub> (N+1) \u2264 (h+1) * log<sub>2<\/sub> 2 (bring down the exponent)<br>log<sub>2<\/sub> (N+1) \u2264 h+1 (log<sub>2<\/sub> 2 is 1)<br>h+1 \u2265 log<sub>2<\/sub> (N+1) (flip the direction)<br>h \u2265 log<sub>2<\/sub> (N+1)-1 (apply -1 on both sides)<br><\/pre>","title":"Derivation of the Lower Bound"},{"id":363,"category":"bst","order":7,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 03:17:17","updated_at":"2023-10-17 07:54:04","section":319,"code":"$(\"#title-BST\").click();\nskewed('right');","section_order":13,"value":"13-7","text":"<p>If we have <b>N<\/b> elements\/items\/keys in our BST, the upper bound height <b>h<\/b> = O(<b>N<\/b>) if we insert the elements in ascending order (to get skewed right BST as shown above).<\/p><br><p>The height of such BST is <samp>h = N-1<\/samp>, so we have <samp>h &lt; N<\/samp>.<\/p><br><p>Discussion: Do you know how to get skewed left BST instead?<\/p>","title":"The Upper Bound of BST Height"},{"id":384,"category":"bst","order":8,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 13:59:21","updated_at":"2018-03-12 12:30:12","section":319,"code":"","section_order":13,"value":"13-8","text":"<p>Very simple, insert the elements in descending order (from empty BST).<\/p>","title":"The Solution"},{"id":364,"category":"bst","order":9,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 06:16:05","updated_at":"2018-03-12 12:30:09","section":319,"code":"$(\"#title-AVL\").click();\nexample(3);","section_order":13,"value":"13-9","text":"<p>We have seen that most BST operations are in O(<b>h<\/b>) and combining the lower and upper bounds of <b>h<\/b>, we have log<sub>2<\/sub> <b>N<\/b> &lt; <b>h<\/b> &lt; <b>N<\/b>.<\/p><br><p>There is a dramatic difference between log<sub>2<\/sub> <b>N<\/b> and <b>N<\/b> and we have seen from the discussion of the lower bound that getting perfect BST (at all times) is near impossible...<\/p><br><p>So can we have BST that has height closer to log<sub>2<\/sub> <b>N<\/b>, i.e. <b>c<\/b> * log<sub>2<\/sub> <b>N<\/b>, for a small constant factor <b>c<\/b>? If we can, then BST operations that run in O(<b>h<\/b>) actually run in O(log <b>N<\/b>)...<\/p>","title":"The Combined Bound"},{"id":359,"category":"bst","order":14,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 14:28:28","updated_at":"2023-05-26 17:35:20","section":-1,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":-1,"value":"14","text":"<p>Introducing AVL Tree, invented by two Russian (Soviet) inventors: Georgy Adelson-Velskii and Evgenii Landis, back in 1962.<\/p><br><p>In AVL Tree, we will later see that its height <b>h<\/b> &lt; 2 * log <b>N<\/b> (tighter analysis exist, but we will use easier analysis in VisuAlgo where <b>c = 2<\/b>). Therefore, most AVL Tree operations run in O(log <b>N<\/b>) time &mdash; efficient.<\/p><br><p>Insert(v) and Remove(v) update operations may change the height <b>h<\/b> of the AVL Tree, but we will see <b>rotation<\/b> operation(s) to maintain the AVL Tree height to be low.<\/p>","title":"AVL Tree"},{"id":365,"category":"bst","order":1,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 06:33:35","updated_at":"2023-05-26 17:35:24","section":359,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":14,"value":"14-1","text":"<p>To have efficient performance, we shall not maintain <b>height(v)<\/b> attribute via the O(<b>N<\/b>) recursive method every time there is an update (Insert(v)\/Remove(v)) operation.<\/p><br><p>Instead, we compute O(<b>1<\/b>): <samp>x.height = max(x.left.height, x.right.height) + 1<\/samp> at the back of our Insert(v)\/Remove(v) operation as only the height of vertices along the insertion\/removal path may be affected. Thus, only O(<b>h<\/b>) vertices may change its <b>height(v)<\/b> attribute and in AVL Tree, <b>h<\/b> &lt; 2 * log <b>N<\/b>.<\/p><br><p>Try <span class=\"slide-actions\" onclick=\"doButtonAction69()\">Insert(37)<\/span> on the example AVL Tree (ignore the resulting rotation for now, we will come back to it in the next few slides). Notice that only a few vertices along the insertion path: {41,20,29,32} increases their height by +1 and all other vertices will have their heights unchanged.<\/p>","title":"Step 1: Maintaining height(v) Efficiently"},{"id":366,"category":"bst","order":2,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 06:51:53","updated_at":"2023-05-26 17:35:27","section":359,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":14,"value":"14-2","text":"<p>Let&#39;s define the following important AVL Tree invariant (property that will never change): A vertex <b>v<\/b> is said to be <b>height-balanced<\/b> if <samp>|v.left.height - v.right.height| &le; 1<\/samp>.<\/p><br><p>A BST is called height-balanced according to the invariant above if every vertex in the BST is height-balanced. Such BST is called AVL Tree, like the example shown above.<\/p><br><p>Take a moment to pause here and try inserting a few new random vertices or deleting a few random existing vertices. Will the resulting BST still considered height-balanced?<\/p>","title":"Step 2: Define AVL Tree Invariant"},{"id":367,"category":"bst","order":3,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 07:18:28","updated_at":"2023-05-26 17:35:30","section":359,"code":"$(\"#title-AVL\").click();\nexample(5);","section_order":14,"value":"14-3","text":"<p>Adelson-Velskii and Landis claim that an AVL Tree (a height-balanced BST that satisfies AVL Tree invariant) with <b>N<\/b> vertices has height <b>h<\/b> &lt; 2 * log<sub>2<\/sub> <b>N<\/b>.<\/p><br><p>The proof relies on the concept of minimum-size AVL Tree of a certain height <b>h<\/b>.<\/p><br><p>Let <b>N<sub>h<\/sub><\/b> be the minimum number of vertices in a height-balanced AVL Tree of height <b>h<\/b>.<\/p><br><p>The first few values of <b>N<sub>h<\/sub><\/b> are <b>N<sub>0<\/sub> = 1<\/b> (a single root vertex), <b>N<sub>1<\/sub> = 2<\/b> (a root vertex with either one left child or one right child only), <b>N<sub>2<\/sub> = 4<\/b>, <b>N<sub>3<\/sub> = 7<\/b>, <b>N<sub>4<\/sub> = 12<\/b>, <b>N<sub>5<\/sub> = 20<\/b> (see the background picture), and so on (see the next two slides).<\/p>","title":"Proof - 1"},{"id":661,"category":"bst","order":4,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-10-13 07:02:37","updated_at":"2023-05-26 17:35:32","section":359,"code":"$(\"#title-AVL\").click();\nexample(5);","section_order":14,"value":"14-4","text":"<p>We know that for any other AVL Tree of <b>N<\/b> vertices (not necessarily the minimum-size one), we have <b>N \u2265 N<sub>h<\/sub><\/b>.<\/p><br><img src=\"https:\/\/visualgo.net\/img\/bst_min_avl1.png\" alt=\"Proof-2\"><br><p>In the background picture, we have <b>N<sub>5<\/sub> = 20<\/b> vertices but we know that we can squeeze 43 more vertices (up to <b>N = 63<\/b>) before we have a perfect binary tree of height <b>h = 5<\/b>.<\/p>","title":"Proof - 2"},{"id":659,"category":"bst","order":5,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-10-13 06:25:13","updated_at":"2023-06-06 13:43:39","section":359,"code":"$(\"#title-AVL\").click();\nexample(5);","section_order":14,"value":"14-5","text":"<pre>N<sub>h<\/sub> = 1 + N<sub>h-1<\/sub> + N<sub>h-2<\/sub> (formula for minimum-size AVL tree of height h)<br>N<sub>h<\/sub> &gt; 1 + 2*N<sub>h-2<\/sub> (as N<sub>h-1<\/sub> > N<sub>h-2<\/sub>)<br>N<sub>h<\/sub> &gt; 2*N<sub>h-2<\/sub> (obviously)<br>N<sub>h<\/sub> &gt; 4*N<sub>h-4<\/sub> (recursive)<br>N<sub>h<\/sub> &gt; 8*N<sub>h-6<\/sub> (another recursive step)<br>... (we can only do this h\/2 times, assuming initial h is even)<br>N<sub>h<\/sub> &gt; 2<sup>h\/2<\/sup>*N<sub>0<\/sub> (we reach base case)<br>N<sub>h<\/sub> &gt; 2<sup>h\/2<\/sup> (as N<sub>0<\/sub> = 1)<\/pre><center><img style=\"width: 70%\" src=\"https:\/\/visualgo.net\/img\/bst_min_avl2.png\" alt=\"Proof-3\"><\/center>","title":"Proof - 3"},{"id":660,"category":"bst","order":6,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-10-13 06:32:30","updated_at":"2023-06-06 13:44:16","section":359,"code":"$(\"#title-AVL\").click();\nexample(5);","section_order":14,"value":"14-6","text":"<pre>N &ge; N<sub>h<\/sub> &gt; 2<sup>h\/2<\/sup> (combining the previous two slides)<br>N &gt; 2<sup>h\/2<\/sup><br>log<sub>2<\/sub>(N) &gt; log<sub>2<\/sub>(2<sup>h\/2<\/sup>) (log<sub>2<\/sub> on both sides)<br>log<sub>2<\/sub>(N) &gt; h\/2 (formula simplification)<br>2 * log<sub>2<\/sub>(N) &gt; h or h &lt; 2 * log<sub>2<\/sub>(N)<br>h = O(log(N)) (the final conclusion)<\/pre><center><img style=\"width: 30%\" src=\"https:\/\/visualgo.net\/img\/bst_min_avl3.png\" alt=\"Proof-4\"><\/center>","title":"Proof - 4"},{"id":368,"category":"bst","order":7,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 07:35:11","updated_at":"2023-05-26 17:35:44","section":359,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":14,"value":"14-7","text":"<p>Look at the example BST again. See that all vertices are height-balanced, an AVL Tree.<\/p><br><p>To quickly detect if a vertex <b>v<\/b> is height balanced or not, we modify the AVL Tree invariant (that has absolute function inside) into: <samp>bf(v) = v.left.height - v.right.height<\/samp>.<\/p><br><p>Now try <span class=\"slide-actions\" onclick=\"doButtonAction69()\">Insert(37)<\/span> on the example AVL Tree again. A few vertices along the insertion path: {41,20,29,32} increases their height by +1. Vertices {29,20} will no longer be height-balanced after this insertion (and will be rotated later &mdash; discussed in the next few slides), i.e. bf(29) = -2 and bf(20) = -2 too. We need to restore the balance.<\/p>","title":"Step 3: Maintain Invariant"},{"id":369,"category":"bst","order":8,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 08:02:23","updated_at":"2023-09-25 09:48:51","section":359,"code":"","section_order":14,"value":"14-8","text":"<img src=\"https:\/\/visualgo.net\/img\/tree_rotation.png\" alt=\"Tree Rotation\" width=\"500\"><br><p>See the picture above. Calling <b>rotateRight(D)<\/b> on the left picture will produce the right picture. Calling <b>rotateLeft(B)<\/b> on the right picture will produce the left picture again.<\/p><br><p><b>rotateRight(T)<\/b>\/<b>rotateLeft(T)<\/b> can only be called if <b>T<\/b> has a left\/right child, respectively.<\/p><br><p>Tree Rotation <b>preserves<\/b> BST property.<br>Before rotation, A &lt; B &lt; C &lt; D &lt; E.<br>After rotation, notice that subtree rooted at C (if it exists) changes parent,<br>but the order of A &lt; B &lt; C &lt; D &lt; E does not change.<\/p>","title":"Introducing Tree Rotation"},{"id":370,"category":"bst","order":9,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 08:16:36","updated_at":"2023-05-26 17:37:08","section":359,"code":"","section_order":14,"value":"14-9","text":"<pre>BSTVertex rotateLeft(BSTVertex T) \/\/ pre-req: T.right != null<br>  BSTVertex w = T.right \/\/ rotateRight is the mirror copy of this<br>  w.parent = T.parent \/\/ this method is hard to get right for newbie<br>  T.parent = w<br>  T.right = w.left<br>  if (w.left != null) w.left.parent = T<br>  w.left = T<br>  \/\/ update the height of T and then w here<br>  return w<\/pre>","title":"Non-trivial O(1) Tree Rotation Pseudo-code"},{"id":373,"category":"bst","order":10,"top":"70px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 09:15:48","updated_at":"2023-09-25 08:16:29","section":359,"code":"","section_order":14,"value":"14-10","text":"<img src=\"https:\/\/visualgo.net\/img\/four_cases.png\" alt=\"Four Cases\" width=\"500\"><br><p>There are only these four cases:<\/p><ol><li>Left Left Case: bf(F) = +2 and bf(D) = +1, solution: rotateRight(F)<\/li><li>Left Right Case: bf(F) = +2 and bf(B) = -1, solution: rotateLeft(B) first to transform this case into Left Left Case again, then go to step 1<\/li><li>Right Right Case: bf(B) = -2 and bf(D) = -1, solution: rotateLeft(B)<\/li><li>Right Left Case: bf(B) = -2 and bf(F) = +1, solution: rotateRight(F) first to transform this case into Right Right Case again, then go to step 3<\/li><\/ol>","title":"Four Rebalancing Cases"},{"id":371,"category":"bst","order":11,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 08:20:59","updated_at":"2023-05-26 17:36:03","section":359,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":14,"value":"14-11","text":"<ol><li>Just insert <b>v<\/b> as in normal BST,<\/li><li>Walk up the AVL Tree from the insertion point back to the root and at every step, we update the height and balance factor of the affected vertices:<ol type=\"a\"><li>Stop at the <b>first<\/b> vertex that is out-of-balance (+2 or -2), if any,<\/li><li>Use <b>one<\/b> of the four tree rotation cases to rebalance it again, e.g. try <span class=\"slide-actions\" onclick=\"doButtonAction69()\">Insert(37)<\/span> on the example above and notice by calling <b>rotateLeft(29)<\/b> once, we fix the imbalance issue.<\/li><\/ol><\/li><\/ol><p>Discussion: Is there other tree rotation cases for Insert(v) operation of AVL Tree?<\/p>","title":"Insert(v) in AVL Tree"},{"id":385,"category":"bst","order":12,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 14:17:08","updated_at":"2023-05-26 17:36:06","section":359,"code":"$(\"#title-AVL\").click();\nexample(2);","section_order":14,"value":"14-12","text":"<p>There is no other case.<\/p><br><p>Insert(v) may indeed cause more than one vertex along the insertion path to have its height increase by one unit.<\/p><br><p>However, as soon as we fix the lowest vertex <b>x<\/b> that is out-of-balance by a bit (+2 or -2), the subsequent one (or double) rotation(s) will make the height of vertex <b>x<\/b> decreases by one again. Thus, any other vertices above <b>x<\/b> along the insertion path will no longer be out-of-balance anymore.<\/p>","title":"The Answer"},{"id":372,"category":"bst","order":13,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 08:26:08","updated_at":"2023-05-26 17:36:09","section":359,"code":"$(\"#title-AVL\").click();\nexample(4);","section_order":14,"value":"14-13","text":"<ol><li>Just remove <b>v<\/b> as in normal BST (one of the three removal cases),<\/li><li>Walk up the AVL Tree from the deletion point back to the root and at every step, we update the height and balance factor of the affected vertices:<ol><li>Now for <b>every<\/b> vertex that is out-of-balance (+2 or -2), we use <b>one<\/b> of the four tree rotation cases to rebalance <b>them<\/b> (can be more than one) again.<\/li><\/ol><\/li><\/ol><p>The main difference compared to Insert(v) in AVL tree is that we may trigger one of the four possible rebalancing cases <b>several times<\/b>, but not more than <b>h<\/b> = O(log <b>N<\/b>) times :O, try <span class=\"slide-actions\" onclick=\"doButtonAction68()\">Remove(7)<\/span> on the example above to see two chain reactions <b>rotateRight(6)<\/b> and then <b>rotateRight(16)+rotateLeft(8)<\/b> combo.<\/p>","title":"Remove(v) in AVL Tree"},{"id":375,"category":"bst","order":14,"top":"310px","right":"","bottom":"","left":"50%","marginLeft":"-250px","width":"500px","showActionsPanel":1,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-13 09:40:19","updated_at":"2025-10-13 04:20:10","section":359,"code":"$(\"#title-AVL\").click();\nexample(5);","section_order":14,"value":"14-14","text":"<p>We have now see how AVL Tree defines the height-balance invariant, maintain it for all vertices during Insert(v) and Remove(v) update operations, and a proof that AVL Tree has <b>h<\/b> &lt; 2 * log <b>N<\/b>.<\/p><br><p>Therefore, <b>all<\/b> BST operations (both update and query operations except Inorder Traversal) that we have learned so far, if they have time complexity of O(<b>h<\/b>), they have time complexity of O(log <b>N<\/b>) if we use AVL Tree version of BST.<\/p><br><p>This marks the end of this e-Lecture, but please switch to &#39;Exploration Mode&#39; and try making various calls to Insert(v) and Remove(v) in AVL Tree mode to strengthen your understanding of this data structure.<\/p><hr><p>PS: If you want to study how these seemingly complex AVL Tree (rotation) operations are implemented in a real program, you can download this <a href=\"https:\/\/github.com\/stevenhalim\/cpbook-code\/blob\/master\/ch2\/nonlineards\/AVL.cpp\" target=\"_blank\"><u>AVLDemo.cpp<\/u><\/a> | <a href=\"https:\/\/github.com\/stevenhalim\/cpbook-code\/blob\/master\/ch2\/nonlineards\/AVL.java\" target=\"_blank\"><u>java<\/u><\/a> (must be used together with this <a href=\"http:\/\/www.comp.nus.edu.sg\/~stevenha\/cs2040\/demos\/BSTDemo.cpp\" target=\"_blank\"><u>BSTDemo.cpp<\/u><\/a> | <a href=\"http:\/\/www.comp.nus.edu.sg\/~stevenha\/cs2040\/demos\/BSTDemo.java\" target=\"_blank\"><u>java<\/u><\/a>).<\/p>","title":"AVL Tree Summary"},{"id":352,"category":"bst","order":15,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-12 09:09:12","updated_at":"2023-05-26 17:37:56","section":-1,"code":"","section_order":-1,"value":"15","text":"<p>We will end this module with a few more interesting things about BST and balanced BST (especially AVL Tree).<\/p>","title":"Extras"},{"id":386,"category":"bst","order":1,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 14:31:12","updated_at":"2023-05-26 17:38:00","section":352,"code":"","section_order":15,"value":"15-1","text":"<p>You have seen how we augment height(v) attribute for AVL Tree rebalancing purposes. We now augment size(v) attribute too: The number of elements in the subtree of the BST rooted at <b>v<\/b>. We can maintain size(v) attribute during every insertion and deletion to AVL Tree as with height(v).<\/p><br><p>rank(v) = size(v.left)+1 (think about it).<\/p><br><p>For select(k), if rank(root) is k, we stop, otherwise we know which subtree to recurse on (think about it).<\/p>","title":"Those 2 Extra BST Operations"},{"id":387,"category":"bst","order":2,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 14:36:11","updated_at":"2023-05-26 17:38:02","section":352,"code":"","section_order":15,"value":"15-2","text":"<p>In <a href=\".\/heap\"><u>Binary Heap<\/u><\/a> module, we learned an efficient data structure to implement Priority Queue ADT.<\/p><br><p>If you do not already realize it, we can also use BST, to be precise: any <b>balanced<\/b> BST, to implement Priority Queue ADT too. How?<\/p>","title":"Side Usage of Balanced BST?"},{"id":388,"category":"bst","order":3,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-16 14:36:17","updated_at":"2023-05-26 17:39:15","section":352,"code":"","section_order":15,"value":"15-3","text":"<p>For a few more interesting questions about this data structure, please practice on <a href=\"https:\/\/visualgo.net\/training?diff=Medium&amp;n=7&amp;tl=0&amp;module=bst,avl\"><u>BST\/AVL<\/u><\/a> training module (no login is required).<\/p><br><p>However, for registered users, you should login and click the training icon from the homepage to officially clear this module and such achievement will be recorded in your user account.<\/p>","title":"Online Quiz"},{"id":389,"category":"bst","order":4,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":0,"created_at":"2017-05-16 14:38:53","updated_at":"2023-05-26 17:38:07","section":352,"code":"","section_order":15,"value":"15-4","text":"<p>We also have a few programming problems that somewhat requires the usage of this <b>balanced<\/b> BST (like AVL Tree) data structure: <a href=\"https:\/\/open.kattis.com\/problems\/compoundwords\" title=\"\" target=\"_blank\"><u>Kattis - compoundwords<\/u><\/a> and <a href=\"https:\/\/open.kattis.com\/problems\/baconeggsandspam\" title=\"\" target=\"_blank\"><u>Kattis - baconeggsandspam<\/u><\/a>.<\/p><br><p>Try them to consolidate and improve your understanding about this data structure. You are allowed to use C++ STL map\/set, Java TreeMap\/TreeSet, or OCaml <a href=\"https:\/\/caml.inria.fr\/pub\/docs\/manual-ocaml\/libref\/Map.html\" target=\"_blank\"><u>Map<\/u><\/a>\/<a href=\"https:\/\/caml.inria.fr\/pub\/docs\/manual-ocaml\/libref\/Set.html\" target=\"_blank\"><u>Set<\/u><\/a> if that simplifies your implementation (Note that Python doesn&#39;t have built-in bBST implementation).<\/p>","title":"Online Judge Exercises"},{"id":390,"category":"bst","order":5,"top":"70px","right":"","bottom":"","left":"60px","marginLeft":"","width":"500px","showActionsPanel":0,"showStatusPanel":0,"showCodetracePanel":1,"created_at":"2017-05-16 14:41:44","updated_at":"2023-05-26 17:38:10","section":352,"code":"","section_order":15,"value":"15-5","text":"<p>The two selected problems are trivial actually...<br><\/p>","title":"The Solution"}];
      const numSlides = lectureIds.length;
      var sectorJunction12Section = 0, sectorJunction12Slide = 0;
      var sectorJunction23Section = 0, sectorJunction23Slide = 0;
      var sector1Count = 0, sector2Count = 0, sector3Count = 0;
      const sectorLength = Math.floor(numSlides / 3);
      function createELectureTimelineDisplay() {
        for (let j = 0; j < numSlides; ++j) {
          const currLecture = lectureIds[j].value;
          if (currLecture.includes('-')) {
            $('#e-lecture-timeline').append(
              $(`<div class="e-lecture-timeline-slide" slideNo=${lectureIds[j].value}></div>`)
            );
          } else {
            $('#e-lecture-timeline').append(
              $(`<div class="e-lecture-timeline-checkpoint" slideNo=${lectureIds[j].value}></div>`)
            );
          }
        }
      }

      function setSectorJunctionInfo() {
          //setting the sector junction slide numbers
          const j12 = sectorLength !== 0 ? (sectorLength - 1): 0;
          const j23 = sectorLength !== 0 ? (2 * sectorLength - 1) : 0;

          const sectorJunction12 = lectureIds[j12].value.split('-');
          sectorJunction12Section = parseInt(sectorJunction12[0]);
          sectorJunction12Slide = sectorJunction12.length > 1 ? parseInt(sectorJunction12[1]) : sectorJunction12Slide;

          const sectorJunction23 = lectureIds[j23].value.split('-');
          sectorJunction23Section = parseInt(sectorJunction23[0]);
          sectorJunction23Slide = sectorJunction23.length > 1 ? parseInt(sectorJunction23[1]) : sectorJunction23Slide;
      }

      function runSlide(slide) { // Steven's patch on 28 Jan 2022: Properly remove slide 99, 99-1, 99-2, 99-3, integrate with the earlier slides
        if (slide == '1') {
          $("#e-lecture").html("slide " + slide + " (" + 1 + "%)");
          
        }
        if (slide == '2') {
          $("#e-lecture").html("slide " + slide + " (" + 2 + "%)");
          
        }
        if (slide == '3') {
          $("#e-lecture").html("slide " + slide + " (" + 3 + "%)");
          
        }
        if (slide == '3-1') {
          $("#e-lecture").html("slide " + slide + " (" + 5 + "%)");
          
        }
        if (slide == '3-2') {
          $("#e-lecture").html("slide " + slide + " (" + 6 + "%)");
          
        }
        if (slide == '3-3') {
          $("#e-lecture").html("slide " + slide + " (" + 7 + "%)");
          
        }
        if (slide == '3-4') {
          $("#e-lecture").html("slide " + slide + " (" + 9 + "%)");
          const logn_value = document.querySelector("#logn");
const n_value = document.querySelector("#n");
const input = document.querySelector("#logn_input");
logn_value.textContent = input.value;
n_value.textContent = Math.pow(2, input.value);
input.addEventListener("input", (event) => {
  logn_value.textContent = event.target.value;
  n_value.textContent = Math.pow(2, event.target.value);
})
        }
        if (slide == '3-5') {
          $("#e-lecture").html("slide " + slide + " (" + 10 + "%)");
          
        }
        if (slide == '3-6') {
          $("#e-lecture").html("slide " + slide + " (" + 11 + "%)");
          
        }
        if (slide == '3-7') {
          $("#e-lecture").html("slide " + slide + " (" + 13 + "%)");
          
        }
        if (slide == '3-8') {
          $("#e-lecture").html("slide " + slide + " (" + 14 + "%)");
          
        }
        if (slide == '3-9') {
          $("#e-lecture").html("slide " + slide + " (" + 15 + "%)");
          
        }
        if (slide == '3-10') {
          $("#e-lecture").html("slide " + slide + " (" + 17 + "%)");
          
        }
        if (slide == '4') {
          $("#e-lecture").html("slide " + slide + " (" + 18 + "%)");
          $("#title-BST").click();
example(1);
        }
        if (slide == '4-1') {
          $("#e-lecture").html("slide " + slide + " (" + 19 + "%)");
          $("#title-BST").click();
example(1);
        }
        if (slide == '4-2') {
          $("#e-lecture").html("slide " + slide + " (" + 21 + "%)");
          
        }
        if (slide == '4-3') {
          $("#e-lecture").html("slide " + slide + " (" + 22 + "%)");
          $("#title-BST").click();
example(1);
        }
        if (slide == '5') {
          $("#e-lecture").html("slide " + slide + " (" + 23 + "%)");
          $("#search").addClass("menu-highlighted");
$("#predsucc").addClass("menu-highlighted");
$("#traverse").addClass("menu-highlighted");
$("#insert").addClass("menu-highlighted");
$("#remove").addClass("menu-highlighted");
$("#create").addClass("menu-highlighted");
        }
        if (slide == '5-1') {
          $("#e-lecture").html("slide " + slide + " (" + 25 + "%)");
          
        }
        if (slide == '5-2') {
          $("#e-lecture").html("slide " + slide + " (" + 26 + "%)");
          $("#insert").addClass("menu-highlighted");
$("#remove").addClass("menu-highlighted");
        }
        if (slide == '6') {
          $("#e-lecture").html("slide " + slide + " (" + 27 + "%)");
          $("#search").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '6-1') {
          $("#e-lecture").html("slide " + slide + " (" + 28 + "%)");
          $("#search").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '6-2') {
          $("#e-lecture").html("slide " + slide + " (" + 30 + "%)");
          $("#search").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '6-3') {
          $("#e-lecture").html("slide " + slide + " (" + 31 + "%)");
          $("#search").click().addClass("menu-highlighted");
$("#title-BST").click();
skewed('right');
        }
        if (slide == '7') {
          $("#e-lecture").html("slide " + slide + " (" + 32 + "%)");
          $("#predsucc").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '7-1') {
          $("#e-lecture").html("slide " + slide + " (" + 34 + "%)");
          $("#predsucc").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '7-2') {
          $("#e-lecture").html("slide " + slide + " (" + 35 + "%)");
          $("#predsucc").click().addClass("menu-highlighted");
$("#title-BST").click();
skewed('right');
        }
        if (slide == '8') {
          $("#e-lecture").html("slide " + slide + " (" + 36 + "%)");
          $("#traverse").click().addClass("menu-highlighted");
$("#inorder-go").addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '8-1') {
          $("#e-lecture").html("slide " + slide + " (" + 38 + "%)");
          $("#traverse").click().addClass("menu-highlighted");
$("#inorder-go").addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '8-2') {
          $("#e-lecture").html("slide " + slide + " (" + 39 + "%)");
          $("#traverse").click().addClass("menu-highlighted");
$("#inorder-go").addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '8-3') {
          $("#e-lecture").html("slide " + slide + " (" + 40 + "%)");
          $("#traverse").click().addClass("menu-highlighted");
$("#preorder-go").addClass("menu-highlighted");
$("#postorder-go").addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '8-4') {
          $("#e-lecture").html("slide " + slide + " (" + 42 + "%)");
          $("#traverse").click().addClass("menu-highlighted");
$("#preorder-go").addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '9') {
          $("#e-lecture").html("slide " + slide + " (" + 43 + "%)");
          $("#insert").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '9-1') {
          $("#e-lecture").html("slide " + slide + " (" + 44 + "%)");
          $("#insert").click().addClass("menu-highlighted");
$("#title-BST").click();
skewed('right');
        }
        if (slide == '9-2') {
          $("#e-lecture").html("slide " + slide + " (" + 46 + "%)");
          
        }
        if (slide == '10') {
          $("#e-lecture").html("slide " + slide + " (" + 47 + "%)");
          $("#remove").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '10-1') {
          $("#e-lecture").html("slide " + slide + " (" + 48 + "%)");
          $("#remove").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '10-2') {
          $("#e-lecture").html("slide " + slide + " (" + 50 + "%)");
          $("#remove").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '10-3') {
          $("#e-lecture").html("slide " + slide + " (" + 51 + "%)");
          $("#remove").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '10-4') {
          $("#e-lecture").html("slide " + slide + " (" + 52 + "%)");
          $("#remove").click().addClass("menu-highlighted");
$("#title-BST").click();
example(1);
        }
        if (slide == '10-5') {
          $("#e-lecture").html("slide " + slide + " (" + 53 + "%)");
          
        }
        if (slide == '10-6') {
          $("#e-lecture").html("slide " + slide + " (" + 55 + "%)");
          $("#remove").click().addClass("menu-highlighted");
$("#title-BST").click();
skewed('right');
        }
        if (slide == '11') {
          $("#e-lecture").html("slide " + slide + " (" + 56 + "%)");
          $("#create").click().addClass("menu-highlighted");
        }
        if (slide == '12') {
          $("#e-lecture").html("slide " + slide + " (" + 57 + "%)");
          $("#title-BST").click();
skewed('left');
        }
        if (slide == '12-1') {
          $("#e-lecture").html("slide " + slide + " (" + 59 + "%)");
          
        }
        if (slide == '13') {
          $("#e-lecture").html("slide " + slide + " (" + 60 + "%)");
          $("#title-BST").click();
skewed('right');
        }
        if (slide == '13-1') {
          $("#e-lecture").html("slide " + slide + " (" + 61 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '13-2') {
          $("#e-lecture").html("slide " + slide + " (" + 63 + "%)");
          
        }
        if (slide == '13-3') {
          $("#e-lecture").html("slide " + slide + " (" + 64 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '13-4') {
          $("#e-lecture").html("slide " + slide + " (" + 65 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '13-5') {
          $("#e-lecture").html("slide " + slide + " (" + 67 + "%)");
          $("#title-AVL").click();
example(3);
        }
        if (slide == '13-6') {
          $("#e-lecture").html("slide " + slide + " (" + 68 + "%)");
          $("#title-AVL").click();
example(3);
        }
        if (slide == '13-7') {
          $("#e-lecture").html("slide " + slide + " (" + 69 + "%)");
          $("#title-BST").click();
skewed('right');
        }
        if (slide == '13-8') {
          $("#e-lecture").html("slide " + slide + " (" + 71 + "%)");
          
        }
        if (slide == '13-9') {
          $("#e-lecture").html("slide " + slide + " (" + 72 + "%)");
          $("#title-AVL").click();
example(3);
        }
        if (slide == '14') {
          $("#e-lecture").html("slide " + slide + " (" + 73 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '14-1') {
          $("#e-lecture").html("slide " + slide + " (" + 75 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '14-2') {
          $("#e-lecture").html("slide " + slide + " (" + 76 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '14-3') {
          $("#e-lecture").html("slide " + slide + " (" + 77 + "%)");
          $("#title-AVL").click();
example(5);
        }
        if (slide == '14-4') {
          $("#e-lecture").html("slide " + slide + " (" + 78 + "%)");
          $("#title-AVL").click();
example(5);
        }
        if (slide == '14-5') {
          $("#e-lecture").html("slide " + slide + " (" + 80 + "%)");
          $("#title-AVL").click();
example(5);
        }
        if (slide == '14-6') {
          $("#e-lecture").html("slide " + slide + " (" + 81 + "%)");
          $("#title-AVL").click();
example(5);
        }
        if (slide == '14-7') {
          $("#e-lecture").html("slide " + slide + " (" + 82 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '14-8') {
          $("#e-lecture").html("slide " + slide + " (" + 84 + "%)");
          
        }
        if (slide == '14-9') {
          $("#e-lecture").html("slide " + slide + " (" + 85 + "%)");
          
        }
        if (slide == '14-10') {
          $("#e-lecture").html("slide " + slide + " (" + 86 + "%)");
          
        }
        if (slide == '14-11') {
          $("#e-lecture").html("slide " + slide + " (" + 88 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '14-12') {
          $("#e-lecture").html("slide " + slide + " (" + 89 + "%)");
          $("#title-AVL").click();
example(2);
        }
        if (slide == '14-13') {
          $("#e-lecture").html("slide " + slide + " (" + 90 + "%)");
          $("#title-AVL").click();
example(4);
        }
        if (slide == '14-14') {
          $("#e-lecture").html("slide " + slide + " (" + 92 + "%)");
          $("#title-AVL").click();
example(5);
        }
        if (slide == '15') {
          $("#e-lecture").html("slide " + slide + " (" + 93 + "%)");
          
        }
        if (slide == '15-1') {
          $("#e-lecture").html("slide " + slide + " (" + 94 + "%)");
          
        }
        if (slide == '15-2') {
          $("#e-lecture").html("slide " + slide + " (" + 96 + "%)");
          
        }
        if (slide == '15-3') {
          $("#e-lecture").html("slide " + slide + " (" + 97 + "%)");
          
        }
        if (slide == '15-4') {
          $("#e-lecture").html("slide " + slide + " (" + 98 + "%)");
          
        }
        if (slide == '15-5') {
          $("#e-lecture").html("slide " + slide + " (" + 100 + "%)");
          
        }
        clearTimeout(currSlideTimer);
      }

      window.onpopstate = function(event) {
        var slide = event.state['slide'];
        openSlide(slide, function() {
          runSlide(slide);
        });
      };

      function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'), sParameterName, i;

        for (i = 0; i < sURLVariables.length; i++) {
          sParameterName = sURLVariables[i].split('=');
          if (sParameterName[0] === sParam) return sParameterName[1] === undefined ? true : sParameterName[1];
        }
      };
      var slideTimeline = {};

      //reads all visited slides in the slideTimeline and gives them their sector color
      function setVisitedSlideTimelineColors() {
        for(const [sectionNo, visitedSlides] of Object.entries(slideTimeline)) {
          const visitedSlides = slideTimeline[sectionNo];
          for(const visitedSlideNo of visitedSlides) {
            setSlideTimelineColor(visitedSlideNo);
          }
        }
      }

      //only called on load if there is nothing in session
      function setTimelineForCompletedSector(sectorNum) {
        let len = sectorLength;
        switch (sectorNum) {
          case 1 : len = sectorLength; break;
          case 2 : len = 2 * sectorLength; break;
          default: len = numSlides;
        }
        let i = 0;
        switch (sectorNum) {
          case 1 : i = 0; break;
          case 2 : i = sectorLength; break;
          default: i = 2 * sectorLength;
        }
        for (; i < len; i++) {
          saveELectureTimeline(lectureIds[i].value, true);
        }
      }

      function getUserSectorHistory(callback) {
        $.ajax({
          type: 'GET',
          url: "https://visualgo.net/section-info",
          data: {
            _token: "MZUDnINm1oKaTzu2r7f2ZLMT0JysOZNiPJzL2uIN",
            topic: "/bst".substring(1)
          }
        }
        ).done(function (data) {
            if (data.data[0] === 1) {
              setF1SectorColor(1);
              setTimelineForCompletedSector(1);
            }
            if (data.data[1] === 1) {
              setF1SectorColor(2);
              setTimelineForCompletedSector(2);
            }
            if (data.data[2] === 1) {
              setF1SectorColor(3);
              setTimelineForCompletedSector(3);
            }
            callback();
        }).fail(function (data) {
            console.log('get user sector history failed!');
        });
      }

      function getELectureTimelineFromSession() {
        const page = "/bst".substring(1);
        const timelineKey = page + '-slide-timeline';
        const storedTimeline = window.sessionStorage.getItem(timelineKey);
        if (storedTimeline) {
          slideTimeline = JSON.parse(storedTimeline);
        } else {
          return false;
        }
        let slideInfo = [];
        for (const [sectionNum, slides] of Object.entries(slideTimeline)) {
          for (const slide of slides) {
            indicateSlideCompletedUI(slide);
            slideInfo = slide.split('-');
            incrementSectorVisits(parseInt(sectionNum), slideInfo.length > 1 ? parseInt(slideInfo[1]) : 0);
          }
        }
        return true;
      }

      async function initializeELectureTimeline() {
        setSectorJunctionInfo();
        if (!getELectureTimelineFromSession())
          getUserSectorHistory(sectorBasedModeSelection);
        else
          sectorBasedModeSelection();

        createELectureTimelineDisplay();
        setVisitedSlideTimelineColors();
      }

      function setF1SectorColor(sectorNum) {
        $(`[sectorNo="${sectorNum}"]`).css('background', sectorColors[(parseInt(sectorNum) % 3)]);
      }

      function updateSectorInDB(sectorNum) {
        $.ajax({
          type: 'POST',
          url: "https://visualgo.net/section-info",
          data: {
            _token: "MZUDnINm1oKaTzu2r7f2ZLMT0JysOZNiPJzL2uIN",
            section: (sectorNum - 1),
            topic: "/bst".substring(1)
          }
        }
        ).done(function (data) {
            //console.log("Saved the sector " + sectorNum + " as done " + JSON.stringify(data));
        }).fail(function (data) {
            console.log("Setting sector done failed new attempt! "+ JSON.stringify(data));
        });
      }

      //If 87.5% or more of the slides in sector are done
      function setF1SectorCompleted(sectorNum, isInitializationCall) {
        setF1SectorColor(sectorNum);
        //avoid api call on initialization
        if (!isInitializationCall) {
          updateSectorInDB(sectorNum);
          $(`[sectorNo="${sectorNum}"]`).css("animation", "green-pulse 2s 4");
          setTimeout(() => {
            $(`[sectorNo="${sectorNum}"]`).css("animation", "");
          }, 8000);
        }
      }

      function incrementSectorVisits(sectionNum, slideNumWithinSection, isInitializationCall) {
        //updating sector count
        if (sectionNum < sectorJunction12Section
          || (sectionNum === sectorJunction12Section && slideNumWithinSection <= sectorJunction12Slide)) {
          ++sector1Count;
          if (sector1Count >= Math.ceil(0.875 * sectorLength))
            setF1SectorCompleted(1, isInitializationCall);
        } else if (sectionNum < sectorJunction23Section
          || (sectionNum === sectorJunction23Section && slideNumWithinSection <= sectorJunction23Slide)) {
          ++sector2Count;
          if (sector2Count >= Math.ceil(0.875 * sectorLength))
            setF1SectorCompleted(2, isInitializationCall);
        } else {
          ++sector3Count;
          if (sector3Count >= Math.ceil(0.875 * (numSlides - 2 * sectorLength)))
            setF1SectorCompleted(3, isInitializationCall);
        }
      }

      function saveELectureTimeline(slideNo, isInitialization) {
        const slideInfo = slideNo.split('-');
        const sectionNo = slideInfo[0];
        const slideNumWithinSection = slideInfo.length > 1 ? parseInt(slideInfo[1]) : 0;
        if (slideTimeline[sectionNo]) {
          if (!slideTimeline[sectionNo].includes(slideNo)) {
            slideTimeline[sectionNo].push(slideNo);
            const sectionNum = parseInt(sectionNo);
            incrementSectorVisits(sectionNum, slideNumWithinSection, isInitialization);
          }
        } else {
          slideTimeline[sectionNo] = [];
          slideTimeline[sectionNo].push(slideNo);
          const sectionNum = parseInt(sectionNo);
          incrementSectorVisits(sectionNum, slideNumWithinSection, isInitialization);
        }
        setSlideTimelineColor(slideNo);
        indicateSlideCompletedUI(slideNo);
      }

      function saveELectureTimelineToSession() {
        const page = "/bst".substring(1);
        const timelineKey = page + '-slide-timeline';
        window.sessionStorage.setItem(timelineKey, JSON.stringify(slideTimeline));
      }

      function handleTimelineOnRunSlide(slideValue) {
        const slideInfo = slideValue.split('-');
        const sectionNo = slideInfo[0];
        const slideNumWithinSection = slideInfo.length > 1 ? parseInt(slideInfo[1]) : 0;
        //start timer only if the slide isnt already done
        if (!slideTimeline[sectionNo] || !slideTimeline[sectionNo].includes(slideValue)) {
          const slideTextLength = $('#electure-'+slideValue + " p").text().length + $('#electure-'+slideValue + " li").text().length;
          const CHARS_READ_PER_MS = 0.05; //when fast, 50 characters a second
          //setting max reading time as 10 seconds for around 500 character slide
          const minSlideReadingTime = Math.min(Math.max(2000, (slideTextLength / CHARS_READ_PER_MS) +  + (2000 * $('#electure-'+slideValue + " img").length)), 10000);
          currSlideTimer = setTimeout(() => {
            saveELectureTimeline(slideValue);
          }, minSlideReadingTime);
        }
      }

      function indicateSlideCompletedUI(slide) {
        $('#electure-'+slide).css("box-shadow", "3px 3px 8px green"); //set green shadow for completed slides
        $('#electure-'+slide + ' .electure-read-status').html("&#10004;");
        $('#electure-'+slide + ' .electure-read-status').attr("title", "Slide Completed!");
        $('#electure-'+slide + ' .electure-read-status').css("font-size", "17px");
      }

      function pushState(slideValue) {
        var url = '/en/bst';
        if (typeof slideValue != 'undefined' && slideValue != null) {
          url += '?slide=' + slideValue;
                  }
        window.history.pushState({slide: slideValue}, "slide " + slideValue, url);
      }

      function showPopup(callback) {
        $('#popup').fadeIn(100, callback);
      }

      function hidePopup(callback) {
        $('#popup').fadeOut(100, callback);
      }

      function showOverlay() {
        $('#overlay').css('opacity', 0.5);
        $('#overlay').show();

        $("#e-lecture-timeline").show();
        $("#e-lecture-f1map").show();
      }

      function hideOverlay() {
        $('#overlay').hide();
        $("#e-lecture").html("");
        $("#e-lecture-timeline").hide();
        $("#e-lecture-f1map").hide();
        clearTimeout(currSlideTimer);
      }

      function makeOverlayTransparent() {
        $('#overlay').css('opacity', 0);
      }

      function hideSlide(callback) {
        isPlaying = true;
        closeSlide(cur_slide, function() {
          makeOverlayTransparent();
          setTimeout(callback, 700); // don't immediately run the animation, wait for 500ms+ first
        });
      }

      function showSlide() {
        isPlaying = false;
        openSlide(cur_slide);
        showOverlay();
      }

      function sectorBasedModeSelection() {
        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());
        //check params are empty and then that all sectors are completed or not
        if (!Object.keys(params).length
          && sector1Count === sectorLength && sector2Count === sectorLength && sector3Count === (numSlides - 2 * sectorLength)) {
            hideOverlay();
        }
        else
          $('#mode-menu a').click();
      }

      $(function() {
        if (isMobileOS() && portraitMatcher.matches) {
          $('#rotateDeviceOverlay').show();
          $('#rotateDeviceText').show();
          $('#widenDeviceText').hide();
          $('#topbar').css("z-index", 10001);
        } else if (matchMediaNarrow.matches) {
          $('#rotateDeviceOverlay').show();
          $('#rotateDeviceText').hide();
          $('#widenDeviceText').show();
          $('#topbar').css("z-index", 10001);
        } else {
          $('#rotateDeviceOverlay').hide();
          $('#topbar').css("z-index", "");
        }

        matchMediaNarrow.addEventListener('change', e => {
          //screws up for square device! NEED RESIZE EVENT
          if (e.matches) {
            if ($('#rotateDeviceOverlay').is(":hidden")) {
              $('#rotateDeviceOverlay').show();
              $('#rotateDeviceText').hide();
              $('#widenDeviceText').show();
              $('#topbar').css("z-index", 10001);
            }
          } else {
            $('#rotateDeviceOverlay').hide();
            $('#topbar').css("z-index", "");
          }
        });
        portraitMatcher.addEventListener('change', e => {
          if (e.matches && isMobileOS()) {
            if ($('#rotateDeviceOverlay').is(":hidden")) {
              $('#rotateDeviceOverlay').show();
              $('#rotateDeviceText').show();
              $('#widenDeviceText').hide();
              $('#topbar').css("z-index", 10001);
            }
          } else {
            $('#rotateDeviceOverlay').hide();
            $('#topbar').css("z-index", "");
          }
        });
        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());
        let slide = getUrlParameter('slide');
        if (typeof slide !== undefined && slide != null) {
          cur_slide = slide;
        }
        //do all timeline and slide stuff only if specific params not provided
        if (!Object.keys(params).length || params["slide"]) {
          if (!isMobileOnLoad) {
                            $('#mode-menu a').click();
                      }
        }
        $('.mcq-submit').click(function() {
          var questionId = parseInt($(this).attr('id').split('-')[1]);
          var answer = $('#mcq-answer-' + questionId).val();
          var userAnswer = $('input[type=radio][name=mcq-'+questionId+'-choice]:checked').val();

          if (answer === userAnswer) {
            $('#answer-status-' + questionId).html('<font color="green"><b>Correct!</b></font>');
          }
          else {
            $('#answer-status-' + questionId).html('<font color="red"><b>Wrong Answer! Try again...</b></font>');
          }
          $('#answer-status-' + questionId).show();
          setTimeout(function() {
            $('#answer-status-' + questionId).fadeOut(1000);
          }, 1000);
        });

        $('.msq-submit').click(function() {
          var questionId = parseInt($(this).attr('id').split('-')[1]);
          var answer = $('#msq-answer-' + questionId).val();

          var answers = [];
          $('input[type=checkbox][class=msq-choice]:checked').each(function() {
            answers.push($(this).attr('id').split('-')[3]);
          });
          answers.sort();
          var userAnswer = answers.join(',');

          if (answer === userAnswer) {
            $('#answer-status-' + questionId).html('<font color="green">Correct!</font>');
          }
          else {
            $('#answer-status-' + questionId).html('<font color="red">Wrong Answer! Try again...</font>');
          }
          $('#answer-status-' + questionId).show();
          setTimeout(function() {
            $('#answer-status-' + questionId).fadeOut(1000);
          }, 1000);
        });

        $('select.lecture-dropdown').change(function() {
          var nextSlide = $(this).val();
          openSlide(nextSlide, function() {
            runSlide(nextSlide);
            pushState(nextSlide);
          });
        });

        $('#hide-popup').click(function() {
          hidePopup();
        });

        $('#popup').hover(function() {
          $('#hide-popup').show();
        }, function() {
          $('#hide-popup').hide();
        });

        $('#electure-1 .electure-next').click(function() {
          hidePopup();
          runSlide('2');
          pushState('2');
        });
        $('#electure-2 .electure-next').click(function() {
          hidePopup();
          runSlide('3');
          pushState('3');
        });
        $('#electure-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('1');
          pushState('1');
        });
        $('#electure-3 .electure-next').click(function() {
          hidePopup();
          runSlide('3-1');
          pushState('3-1');
        });
        $('#electure-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('2');
          pushState('2');
        });
        $('#electure-3-1 .electure-next').click(function() {
          hidePopup();
          runSlide('3-2');
          pushState('3-2');
        });
        $('#electure-3-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('3');
          pushState('3');
        });
        $('#electure-3-2 .electure-next').click(function() {
          hidePopup();
          runSlide('3-3');
          pushState('3-3');
        });
        $('#electure-3-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-1');
          pushState('3-1');
        });
        $('#electure-3-3 .electure-next').click(function() {
          hidePopup();
          runSlide('3-4');
          pushState('3-4');
        });
        $('#electure-3-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-2');
          pushState('3-2');
        });
        $('#electure-3-4 .electure-next').click(function() {
          hidePopup();
          runSlide('3-5');
          pushState('3-5');
        });
        $('#electure-3-4 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-3');
          pushState('3-3');
        });
        $('#electure-3-5 .electure-next').click(function() {
          hidePopup();
          runSlide('3-6');
          pushState('3-6');
        });
        $('#electure-3-5 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-4');
          pushState('3-4');
        });
        $('#electure-3-6 .electure-next').click(function() {
          hidePopup();
          runSlide('3-7');
          pushState('3-7');
        });
        $('#electure-3-6 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-5');
          pushState('3-5');
        });
        $('#electure-3-7 .electure-next').click(function() {
          hidePopup();
          runSlide('3-8');
          pushState('3-8');
        });
        $('#electure-3-7 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-6');
          pushState('3-6');
        });
        $('#electure-3-8 .electure-next').click(function() {
          hidePopup();
          runSlide('3-9');
          pushState('3-9');
        });
        $('#electure-3-8 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-7');
          pushState('3-7');
        });
        $('#electure-3-9 .electure-next').click(function() {
          hidePopup();
          runSlide('3-10');
          pushState('3-10');
        });
        $('#electure-3-9 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-8');
          pushState('3-8');
        });
        $('#electure-3-10 .electure-next').click(function() {
          hidePopup();
          runSlide('4');
          pushState('4');
        });
        $('#electure-3-10 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-9');
          pushState('3-9');
        });
        $('#electure-4 .electure-next').click(function() {
          hidePopup();
          runSlide('4-1');
          pushState('4-1');
        });
        $('#electure-4 .electure-prev').click(function() {
          hidePopup();
          runSlide('3-10');
          pushState('3-10');
        });
        $('#electure-4-1 .electure-next').click(function() {
          hidePopup();
          runSlide('4-2');
          pushState('4-2');
        });
        $('#electure-4-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('4');
          pushState('4');
        });
        $('#electure-4-2 .electure-next').click(function() {
          hidePopup();
          runSlide('4-3');
          pushState('4-3');
        });
        $('#electure-4-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('4-1');
          pushState('4-1');
        });
        $('#electure-4-3 .electure-next').click(function() {
          hidePopup();
          runSlide('5');
          pushState('5');
        });
        $('#electure-4-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('4-2');
          pushState('4-2');
        });
        $('#electure-5 .electure-next').click(function() {
          hidePopup();
          runSlide('5-1');
          pushState('5-1');
        });
        $('#electure-5 .electure-prev').click(function() {
          hidePopup();
          runSlide('4-3');
          pushState('4-3');
        });
        $('#electure-5-1 .electure-next').click(function() {
          hidePopup();
          runSlide('5-2');
          pushState('5-2');
        });
        $('#electure-5-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('5');
          pushState('5');
        });
        $('#electure-5-2 .electure-next').click(function() {
          hidePopup();
          runSlide('6');
          pushState('6');
        });
        $('#electure-5-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('5-1');
          pushState('5-1');
        });
        $('#electure-6 .electure-next').click(function() {
          hidePopup();
          runSlide('6-1');
          pushState('6-1');
        });
        $('#electure-6 .electure-prev').click(function() {
          hidePopup();
          runSlide('5-2');
          pushState('5-2');
        });
        $('#electure-6-1 .electure-next').click(function() {
          hidePopup();
          runSlide('6-2');
          pushState('6-2');
        });
        $('#electure-6-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('6');
          pushState('6');
        });
        $('#electure-6-2 .electure-next').click(function() {
          hidePopup();
          runSlide('6-3');
          pushState('6-3');
        });
        $('#electure-6-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('6-1');
          pushState('6-1');
        });
        $('#electure-6-3 .electure-next').click(function() {
          hidePopup();
          runSlide('7');
          pushState('7');
        });
        $('#electure-6-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('6-2');
          pushState('6-2');
        });
        $('#electure-7 .electure-next').click(function() {
          hidePopup();
          runSlide('7-1');
          pushState('7-1');
        });
        $('#electure-7 .electure-prev').click(function() {
          hidePopup();
          runSlide('6-3');
          pushState('6-3');
        });
        $('#electure-7-1 .electure-next').click(function() {
          hidePopup();
          runSlide('7-2');
          pushState('7-2');
        });
        $('#electure-7-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('7');
          pushState('7');
        });
        $('#electure-7-2 .electure-next').click(function() {
          hidePopup();
          runSlide('8');
          pushState('8');
        });
        $('#electure-7-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('7-1');
          pushState('7-1');
        });
        $('#electure-8 .electure-next').click(function() {
          hidePopup();
          runSlide('8-1');
          pushState('8-1');
        });
        $('#electure-8 .electure-prev').click(function() {
          hidePopup();
          runSlide('7-2');
          pushState('7-2');
        });
        $('#electure-8-1 .electure-next').click(function() {
          hidePopup();
          runSlide('8-2');
          pushState('8-2');
        });
        $('#electure-8-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('8');
          pushState('8');
        });
        $('#electure-8-2 .electure-next').click(function() {
          hidePopup();
          runSlide('8-3');
          pushState('8-3');
        });
        $('#electure-8-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('8-1');
          pushState('8-1');
        });
        $('#electure-8-3 .electure-next').click(function() {
          hidePopup();
          runSlide('8-4');
          pushState('8-4');
        });
        $('#electure-8-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('8-2');
          pushState('8-2');
        });
        $('#electure-8-4 .electure-next').click(function() {
          hidePopup();
          runSlide('9');
          pushState('9');
        });
        $('#electure-8-4 .electure-prev').click(function() {
          hidePopup();
          runSlide('8-3');
          pushState('8-3');
        });
        $('#electure-9 .electure-next').click(function() {
          hidePopup();
          runSlide('9-1');
          pushState('9-1');
        });
        $('#electure-9 .electure-prev').click(function() {
          hidePopup();
          runSlide('8-4');
          pushState('8-4');
        });
        $('#electure-9-1 .electure-next').click(function() {
          hidePopup();
          runSlide('9-2');
          pushState('9-2');
        });
        $('#electure-9-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('9');
          pushState('9');
        });
        $('#electure-9-2 .electure-next').click(function() {
          hidePopup();
          runSlide('10');
          pushState('10');
        });
        $('#electure-9-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('9-1');
          pushState('9-1');
        });
        $('#electure-10 .electure-next').click(function() {
          hidePopup();
          runSlide('10-1');
          pushState('10-1');
        });
        $('#electure-10 .electure-prev').click(function() {
          hidePopup();
          runSlide('9-2');
          pushState('9-2');
        });
        $('#electure-10-1 .electure-next').click(function() {
          hidePopup();
          runSlide('10-2');
          pushState('10-2');
        });
        $('#electure-10-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('10');
          pushState('10');
        });
        $('#electure-10-2 .electure-next').click(function() {
          hidePopup();
          runSlide('10-3');
          pushState('10-3');
        });
        $('#electure-10-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('10-1');
          pushState('10-1');
        });
        $('#electure-10-3 .electure-next').click(function() {
          hidePopup();
          runSlide('10-4');
          pushState('10-4');
        });
        $('#electure-10-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('10-2');
          pushState('10-2');
        });
        $('#electure-10-4 .electure-next').click(function() {
          hidePopup();
          runSlide('10-5');
          pushState('10-5');
        });
        $('#electure-10-4 .electure-prev').click(function() {
          hidePopup();
          runSlide('10-3');
          pushState('10-3');
        });
        $('#electure-10-5 .electure-next').click(function() {
          hidePopup();
          runSlide('10-6');
          pushState('10-6');
        });
        $('#electure-10-5 .electure-prev').click(function() {
          hidePopup();
          runSlide('10-4');
          pushState('10-4');
        });
        $('#electure-10-6 .electure-next').click(function() {
          hidePopup();
          runSlide('11');
          pushState('11');
        });
        $('#electure-10-6 .electure-prev').click(function() {
          hidePopup();
          runSlide('10-5');
          pushState('10-5');
        });
        $('#electure-11 .electure-next').click(function() {
          hidePopup();
          runSlide('12');
          pushState('12');
        });
        $('#electure-11 .electure-prev').click(function() {
          hidePopup();
          runSlide('10-6');
          pushState('10-6');
        });
        $('#electure-12 .electure-next').click(function() {
          hidePopup();
          runSlide('12-1');
          pushState('12-1');
        });
        $('#electure-12 .electure-prev').click(function() {
          hidePopup();
          runSlide('11');
          pushState('11');
        });
        $('#electure-12-1 .electure-next').click(function() {
          hidePopup();
          runSlide('13');
          pushState('13');
        });
        $('#electure-12-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('12');
          pushState('12');
        });
        $('#electure-13 .electure-next').click(function() {
          hidePopup();
          runSlide('13-1');
          pushState('13-1');
        });
        $('#electure-13 .electure-prev').click(function() {
          hidePopup();
          runSlide('12-1');
          pushState('12-1');
        });
        $('#electure-13-1 .electure-next').click(function() {
          hidePopup();
          runSlide('13-2');
          pushState('13-2');
        });
        $('#electure-13-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('13');
          pushState('13');
        });
        $('#electure-13-2 .electure-next').click(function() {
          hidePopup();
          runSlide('13-3');
          pushState('13-3');
        });
        $('#electure-13-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-1');
          pushState('13-1');
        });
        $('#electure-13-3 .electure-next').click(function() {
          hidePopup();
          runSlide('13-4');
          pushState('13-4');
        });
        $('#electure-13-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-2');
          pushState('13-2');
        });
        $('#electure-13-4 .electure-next').click(function() {
          hidePopup();
          runSlide('13-5');
          pushState('13-5');
        });
        $('#electure-13-4 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-3');
          pushState('13-3');
        });
        $('#electure-13-5 .electure-next').click(function() {
          hidePopup();
          runSlide('13-6');
          pushState('13-6');
        });
        $('#electure-13-5 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-4');
          pushState('13-4');
        });
        $('#electure-13-6 .electure-next').click(function() {
          hidePopup();
          runSlide('13-7');
          pushState('13-7');
        });
        $('#electure-13-6 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-5');
          pushState('13-5');
        });
        $('#electure-13-7 .electure-next').click(function() {
          hidePopup();
          runSlide('13-8');
          pushState('13-8');
        });
        $('#electure-13-7 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-6');
          pushState('13-6');
        });
        $('#electure-13-8 .electure-next').click(function() {
          hidePopup();
          runSlide('13-9');
          pushState('13-9');
        });
        $('#electure-13-8 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-7');
          pushState('13-7');
        });
        $('#electure-13-9 .electure-next').click(function() {
          hidePopup();
          runSlide('14');
          pushState('14');
        });
        $('#electure-13-9 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-8');
          pushState('13-8');
        });
        $('#electure-14 .electure-next').click(function() {
          hidePopup();
          runSlide('14-1');
          pushState('14-1');
        });
        $('#electure-14 .electure-prev').click(function() {
          hidePopup();
          runSlide('13-9');
          pushState('13-9');
        });
        $('#electure-14-1 .electure-next').click(function() {
          hidePopup();
          runSlide('14-2');
          pushState('14-2');
        });
        $('#electure-14-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('14');
          pushState('14');
        });
        $('#electure-14-2 .electure-next').click(function() {
          hidePopup();
          runSlide('14-3');
          pushState('14-3');
        });
        $('#electure-14-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-1');
          pushState('14-1');
        });
        $('#electure-14-3 .electure-next').click(function() {
          hidePopup();
          runSlide('14-4');
          pushState('14-4');
        });
        $('#electure-14-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-2');
          pushState('14-2');
        });
        $('#electure-14-4 .electure-next').click(function() {
          hidePopup();
          runSlide('14-5');
          pushState('14-5');
        });
        $('#electure-14-4 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-3');
          pushState('14-3');
        });
        $('#electure-14-5 .electure-next').click(function() {
          hidePopup();
          runSlide('14-6');
          pushState('14-6');
        });
        $('#electure-14-5 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-4');
          pushState('14-4');
        });
        $('#electure-14-6 .electure-next').click(function() {
          hidePopup();
          runSlide('14-7');
          pushState('14-7');
        });
        $('#electure-14-6 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-5');
          pushState('14-5');
        });
        $('#electure-14-7 .electure-next').click(function() {
          hidePopup();
          runSlide('14-8');
          pushState('14-8');
        });
        $('#electure-14-7 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-6');
          pushState('14-6');
        });
        $('#electure-14-8 .electure-next').click(function() {
          hidePopup();
          runSlide('14-9');
          pushState('14-9');
        });
        $('#electure-14-8 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-7');
          pushState('14-7');
        });
        $('#electure-14-9 .electure-next').click(function() {
          hidePopup();
          runSlide('14-10');
          pushState('14-10');
        });
        $('#electure-14-9 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-8');
          pushState('14-8');
        });
        $('#electure-14-10 .electure-next').click(function() {
          hidePopup();
          runSlide('14-11');
          pushState('14-11');
        });
        $('#electure-14-10 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-9');
          pushState('14-9');
        });
        $('#electure-14-11 .electure-next').click(function() {
          hidePopup();
          runSlide('14-12');
          pushState('14-12');
        });
        $('#electure-14-11 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-10');
          pushState('14-10');
        });
        $('#electure-14-12 .electure-next').click(function() {
          hidePopup();
          runSlide('14-13');
          pushState('14-13');
        });
        $('#electure-14-12 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-11');
          pushState('14-11');
        });
        $('#electure-14-13 .electure-next').click(function() {
          hidePopup();
          runSlide('14-14');
          pushState('14-14');
        });
        $('#electure-14-13 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-12');
          pushState('14-12');
        });
        $('#electure-14-14 .electure-next').click(function() {
          hidePopup();
          runSlide('15');
          pushState('15');
        });
        $('#electure-14-14 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-13');
          pushState('14-13');
        });
        $('#electure-15 .electure-next').click(function() {
          hidePopup();
          runSlide('15-1');
          pushState('15-1');
        });
        $('#electure-15 .electure-prev').click(function() {
          hidePopup();
          runSlide('14-14');
          pushState('14-14');
        });
        $('#electure-15-1 .electure-next').click(function() {
          hidePopup();
          runSlide('15-2');
          pushState('15-2');
        });
        $('#electure-15-1 .electure-prev').click(function() {
          hidePopup();
          runSlide('15');
          pushState('15');
        });
        $('#electure-15-2 .electure-next').click(function() {
          hidePopup();
          runSlide('15-3');
          pushState('15-3');
        });
        $('#electure-15-2 .electure-prev').click(function() {
          hidePopup();
          runSlide('15-1');
          pushState('15-1');
        });
        $('#electure-15-3 .electure-next').click(function() {
          hidePopup();
          runSlide('15-4');
          pushState('15-4');
        });
        $('#electure-15-3 .electure-prev').click(function() {
          hidePopup();
          runSlide('15-2');
          pushState('15-2');
        });
        $('#electure-15-4 .electure-next').click(function() {
          hidePopup();
          runSlide('15-5');
          pushState('15-5');
        });
        $('#electure-15-4 .electure-prev').click(function() {
          hidePopup();
          runSlide('15-3');
          pushState('15-3');
        });
        $('#electure-15-5 .electure-prev').click(function() {
          hidePopup();
          runSlide('15-4');
          pushState('15-4');
        });
      });

      function doButtonAction1() {
        CUSTOM_ACTION('search', 7);
      }
      function doButtonAction2() {
        CUSTOM_ACTION('search', 23);
      }
      function doButtonAction3() {
        CUSTOM_ACTION('search', 21);
      }
      function doButtonAction4() {
        $("#v-search").val(64);
mode = "exploration"; 
cur_slide = 1;
$(".tutorial-dialog#tutorial-4").fadeOut(100);
searchVertex(function() {
  mode = "tutorial"; 
  $(".tutorial-dialog#tutorial-4").fadeIn(100);
});
      }
      function doButtonAction5() {
        CUSTOM_ACTION('search', 100);
      }
      function doButtonAction6() {
        CUSTOM_ACTION('successor', 23);
      }
      function doButtonAction52() {
        CUSTOM_ACTION('findmin');
      }
      function doButtonAction53() {
        CUSTOM_ACTION('findmax');
      }
      function doButtonAction54() {
        CUSTOM_ACTION('successor', 7);
      }
      function doButtonAction55() {
        CUSTOM_ACTION('successor', 71);
      }
      function doButtonAction56() {
        CUSTOM_ACTION('predecessor', 6);
      }
      function doButtonAction57() {
        CUSTOM_ACTION('predecessor', 50);
      }
      function doButtonAction58() {
        CUSTOM_ACTION('predecessor', 4);
      }
      function doButtonAction59() {
        CUSTOM_ACTION('inorder');
      }
      function doButtonAction60() {
        CUSTOM_ACTION('insert', 60);
      }
      function doButtonAction61() {
        CUSTOM_ACTION('remove', 5);
      }
      function doButtonAction62() {
        CUSTOM_ACTION('remove', 23);
      }
      function doButtonAction63() {
        CUSTOM_ACTION('remove', 6);
      }
      function doButtonAction64() {
        CUSTOM_ACTION('successor_max');
      }
      function doButtonAction65() {
        CUSTOM_ACTION('insert_max_plus_1');
      }
      function doButtonAction66() {
        CUSTOM_ACTION('remove_max');
      }
      function doButtonAction68() {
        CUSTOM_ACTION('remove', 7);
      }
      function doButtonAction69() {
        CUSTOM_ACTION('insert', 37);
$(this).hide();
      }
      function doButtonAction147() {
        CUSTOM_ACTION('insert', 7);
      }

      $('.electure-print').click((event) => {
        window.open(`/en/bst/print`);
        // Stops overlay from closing just by clicking print.
        event.stopPropagation();
      });
      function adjustPopupToImageSize() {
        var width = $('#popup-image').prop('width');
        var height = $('#popup-image').prop('height');
        $('#popup').width(width + 20);
        $('#popup').height(height + 20);
        if (width == 0 && height == 0) {
          setTimeout(adjustPopupToImageSize, 200);
        } else {
          showPopup();
        }
      }

      function POPUP_IMAGE(url) {
        $('#popup-content').html('<img id="popup-image" src="' + url + '">');
        adjustPopupToImageSize();
      }

      // TODO: This will break something later. Please FIX!
      function OPEN_NEW_URL(url) {
        window.open(url, '_blank');
      }

      // Implement these functions in each visualisation
      // This function will be called before entering e-Lecture Mode
      function ENTER_LECTURE_MODE() {}

      // This function will be called before returning to Explore Mode
      function ENTER_EXPLORE_MODE() {}

      // Lecture action functions
      function CUSTOM_ACTION(action, data, mode) {}

      //
      var GET_SHARE_LINK = undefined;

      // This function will be called everytime 1.0x is changed to 0.5x or vice versa
      function redraw() {}

      $(document).ready(function () {
        setTimeout(function () {
          $('#change-lang-popup').fadeOut('slow')
        }, 5000)
      })

      // Checks after page load whether GET_SHARE_LINK's definition is changed.
      // Is this jank? Yes. But it works!
      $(document).ready(
        function () {
          if (GET_SHARE_LINK !== undefined) {
            $("#trigger-share").show();
            $("#trigger-share").click(function () {
              let shareLink = GET_SHARE_LINK();
              try {
                navigator.clipboard.writeText(shareLink).then(
                  function () {
                    createAlertBox("Copied to clipboard!", "success");
                  },
                  function () {
                    createAlertBox(`Unable to copy. Copy this <a href=\"${shareLink}\"><u>link</u></a>.`, "info");
                  }
                )
              } catch (e) {
                // We add this case because we can't test the behavior on development due to clipboards only being allowed in
                // HTTPS (secure mode).
                // TODO: Make guide to make local development run with HTTPS rather than just HTTP.
                createAlertBox(`Unable to copy. Copy this <a href=\"${shareLink}\"><u>link</u></a>.`, "info");
              }
            }
            );  
          }
        });
      
      
    </script>

<script type="text/javascript">
    var extraCSS = {"traverse":"65px","select":"92px","predsucc":"119px","remove":"146px","insert":"173px","search":"200px","create":"227px","toggle":"254px"};
    var actionsIds = {"toggle":{"p":"Toggle BST Layout","onClick":"bw.toggleLayout()"},"create":{"p":"Create","parents":["create-empty","create-example","create-random","create-skewed"]},"search":{"p":"Search(v)"},"insert":{"p":"Insert(v)"},"remove":{"p":"Remove(v)"},"predsucc":{"p":"Predec-\/Succ-essor(v)"},"select":{"p":"Select(k)"},"traverse":{"p":"Traverse(root)"}};
    var isOpens = {};
    var len = 8;
    var keys = ["toggle","create","search","insert","remove","predsucc","select","traverse"]; 
    for (i = 0; i < len; i++) {
        var actionDetails = keys[i];
        isOpens[actionDetails] = false;
    }
    function openAction(id) {
        hideThirdTiers(id);
        $("." + id).css("bottom", extraCSS[id]);
        if (!isOpens[id]) {
            $('.' + id).fadeIn('fast');
            isOpens[id] = true;
        }
    }
    function closeAction(id) {
        hideThirdTiers(id);
        if (isOpens[id]) {
            $('.' + id).fadeOut('fast');
            $('#' + id + '-err').html("");
            isOpens[id] = false;
        }
    }

    function hideEntireActionsPanel() {
        //hideAllThirdTiers();
                    closeAction('toggle');
                    closeAction('create');
                    closeAction('search');
                    closeAction('insert');
                    closeAction('remove');
                    closeAction('predsucc');
                    closeAction('select');
                    closeAction('traverse');
                hideActionsPanel();
    }

    function hideThirdTiers(tier1Action) {
        if ("parents" in actionsIds[tier1Action]) {
            for (const secondTierAction of actionsIds[tier1Action]["parents"]) {
                $('#' + secondTierAction + '-third-tier').fadeOut('fast');
            }
        }
    }

    function hideAllThirdTiers() {
        for (const tier1Action in actionsIds) {
            hideThirdTiers(tier1Action);
        }
    }

    function toggleChildExtras(tier1, selectedParentTier2) {
        hideThirdTiers(tier1);
        //this actionId must have childExtras
        var style = extraCSS[tier1];
        $("." + tier1).css("bottom", (parseInt(style.substring(0, style.length - 2)) - 27));
        //fade ins and outs are done on the ID whereas css class is set on the class
        //fade in the third tier of the selected 2nd tier parent
        $('#' + selectedParentTier2 + '-third-tier').fadeIn('fast');

        // //fade out all other third tiers of that 'action'
        // for (const parent of actions[tier1]["parents"]) {
        //     console.log("parent is " + parent + " for " + selectedParentTier2);
        //     if (parent != selectedParentTier2) {
        //         $('#' + parent + '-third-tier').fadeOut('fast');
        //     }
        // }
    }

    function setActionHeightOriginal(tier1Action) {
        $("." + tier1Action).css("bottom", extraCSS[tier1Action]);
    }

            $('#' + 'toggle').click(function() {
            openAction('toggle');
                                                                            closeAction('create');
                                                                closeAction('search');
                                                                closeAction('insert');
                                                                closeAction('remove');
                                                                closeAction('predsucc');
                                                                closeAction('select');
                                                                closeAction('traverse');
                                    });
            $('#' + 'create').click(function() {
            openAction('create');
                                                closeAction('toggle');
                                                                                            closeAction('search');
                                                                closeAction('insert');
                                                                closeAction('remove');
                                                                closeAction('predsucc');
                                                                closeAction('select');
                                                                closeAction('traverse');
                                    });
            $('#' + 'search').click(function() {
            openAction('search');
                                                closeAction('toggle');
                                                                closeAction('create');
                                                                                            closeAction('insert');
                                                                closeAction('remove');
                                                                closeAction('predsucc');
                                                                closeAction('select');
                                                                closeAction('traverse');
                                    });
            $('#' + 'insert').click(function() {
            openAction('insert');
                                                closeAction('toggle');
                                                                closeAction('create');
                                                                closeAction('search');
                                                                                            closeAction('remove');
                                                                closeAction('predsucc');
                                                                closeAction('select');
                                                                closeAction('traverse');
                                    });
            $('#' + 'remove').click(function() {
            openAction('remove');
                                                closeAction('toggle');
                                                                closeAction('create');
                                                                closeAction('search');
                                                                closeAction('insert');
                                                                                            closeAction('predsucc');
                                                                closeAction('select');
                                                                closeAction('traverse');
                                    });
            $('#' + 'predsucc').click(function() {
            openAction('predsucc');
                                                closeAction('toggle');
                                                                closeAction('create');
                                                                closeAction('search');
                                                                closeAction('insert');
                                                                closeAction('remove');
                                                                                            closeAction('select');
                                                                closeAction('traverse');
                                    });
            $('#' + 'select').click(function() {
            openAction('select');
                                                closeAction('toggle');
                                                                closeAction('create');
                                                                closeAction('search');
                                                                closeAction('insert');
                                                                closeAction('remove');
                                                                closeAction('predsucc');
                                                                                            closeAction('traverse');
                                    });
            $('#' + 'traverse').click(function() {
            openAction('traverse');
                                                closeAction('toggle');
                                                                closeAction('create');
                                                                closeAction('search');
                                                                closeAction('insert');
                                                                closeAction('remove');
                                                                closeAction('predsucc');
                                                                closeAction('select');
                                                                });
    
    //important to have all the input fields in actions menu take an id containing '-input'
    $("[id*='-input']").on("keypress keydown keyup", (event) => {
        event.stopPropagation();
    });
</script>

<script type="text/javascript">
// BST Widget, also includes AVL tree
// original author: Ivan Reinaldo, then maintained by Steven Halim

var scale = false;
var BST = function() {
  var self = this;

  var valueRange = [-99, 99]; // Range of valid values of BST vertexes allowed (now negatives are allowed on 06 Jun 2023)
  var maxHeightAllowed = 8; // max 8 edges (9 vertices)

  var gw = new GraphWidget(false, true);
  this.getGraphWidget = function() { return gw; };

  var isAVL = false;
  this.getIsAVL = function() { return isAVL; };

  this.isAVL = function(bool) {
    if (typeof bool != 'boolean') return;
    if (bool != isAVL) {
      clearScreen();
      isAVL = bool;
      this.generateRandom();
    }
  };

  /*
   * iBST: Internal representation of BST in this object
   * The keys are the text of the nodes, and the value is the attributes of the corresponding node encapsulated in a JS object, which are:
   * - "parent": text of the parent node. If the node is root node, the value is null.
   * - "leftChild": text of the left child. No child -> null
   * - "rightChild": text of the right child. No child -> null
   * - "cx": X-coordinate of center of the node
   * - "cy": Y-coordinate of center of the node
   * - "vertexClassNumber": Vertex class number of the corresponding node
   * - "height": height of the node. Height of the whole BST is stored at the root
   * - "freq": number of copies of this node, for implementing multiset (26 May 2023 addition)
   * - "sz": size of subtree rooted at this node, for implementing select/rank (07 Jun 2023 addition), number of vertices of the whole BST is the size of the root
   * - "depth": height of the node. Depth of the root is 0, for visualization
   *
   * In addition, there is a key called "root" in iBST, containing the text of the root node.
   * If BST is empty, root is null.
   */

  var iBST = {};
  iBST["root"] = null;

  this.getN = function() { return iBST["root"] == null ? 0 : iBST[iBST["root"]]["sz"]; }
  this.getH = function() { return iBST["root"] == null ? 0 : iBST[iBST["root"]]["height"]; }

  var rankBasedLayout = true;
  this.toggleLayout = function(callback) {
    sl = [];
//console.log("rankBasedLayout = " + rankBasedLayout);
    cs = createState(iBST, {}, {});
    sl.push(cs);

    rankBasedLayout = !rankBasedLayout;
    recalculatePosition();

    cs = createState(iBST, {}, {});
    sl.push(cs);

    gw.startAnimation(sl, callback);
  }

  this.getRandom = function(inBST) {
    var arr = new Array();
    for (var key in iBST) {
      if (key == "root") continue;
      arr.push(key);
    }
    var candidate;
    if (inBST) {
      if (arr.length == 0) // special case for empty BST
        candidate = 1 + Math.floor(Math.random()*99); // [1..99]
      else
        candidate = parseInt(arr[Math.floor(Math.random()*arr.length)]); // one of the key in BST
    }
    else {
      candidate = 1 + Math.floor(Math.random()*99); // [1..99]
      while ($.inArray(candidate, arr) >= 0) // if not -1 (candidate is one of the key in BST)
        candidate = 1 + Math.floor(Math.random()*99); // try again
    }
    return candidate;
  }

  function clearScreen() {
    var key;

    for (key in iBST) {
      if (key == "root") continue;
      gw.removeEdge(iBST[key]["vertexClassNumber"]);
    }

    for (key in iBST) {
      if (key == "root") continue;
      gw.removeVertex(iBST[key]["vertexClassNumber"]);
    }

    iBST = {};
    iBST["root"] = null;
  }

  function init(initArr) {
    clearScreen();

    for (var i = 0; i < initArr.length; ++i) {
      var parentVertex = iBST["root"];
      var newVertex = parseInt(initArr[i]);

      if (parentVertex == null) {
        iBST["root"] = parseInt(newVertex);
        iBST[newVertex] = {
          "parent": null,
          "leftChild": null,
          "rightChild": null,
          "vertexClassNumber": newVertex,
          "freq": 1,
          "depth": 0,
        };
      }
      else {
        while (true) {
          if (parentVertex < newVertex) {
            if (iBST[parentVertex]["rightChild"] == null) break;
            parentVertex = iBST[parentVertex]["rightChild"];
          }
          else {
            if (iBST[parentVertex]["leftChild"] == null) break;
            parentVertex = iBST[parentVertex]["leftChild"];
          }
        }

        if (parentVertex < newVertex)
          iBST[parentVertex]["rightChild"] = newVertex;
        else
          iBST[parentVertex]["leftChild"] = newVertex;

        iBST[newVertex] = {
          "parent": parentVertex,
          "leftChild": null,
          "rightChild": null,
          "vertexClassNumber": newVertex,
          "freq": 1 + (Math.random() < 0.1 ? 1 : 0), // 10% chance for frequency 2 on random keys
        }
      }
    }

    recalculatePosition();

    for (key in iBST) {
      if (key == "root") continue;
      gw.addVertex(iBST[key]["cx"], iBST[key]["cy"], (iBST[key]["freq"] == 1 ? key : (key + '-' + iBST[key]["freq"])), iBST[key]["vertexClassNumber"], true);
    }

    if (iBST["root"] == null)
      $("#info").text("N=0, h=0 (empty BST)");
    else
      $("#info").text("N=" + iBST[iBST["root"]]["sz"] + ", h=" + iBST[iBST["root"]]["height"]);

    for (key in iBST) {
      if (key == "root") continue;
      if (key == iBST["root"]) continue;
      var parentVertex = iBST[key]["parent"];
      gw.addEdge(iBST[parentVertex]["vertexClassNumber"], iBST[key]["vertexClassNumber"], iBST[key]["vertexClassNumber"], EDGE_TYPE_UDE, 1, true);
    }
  }

  this.generate = function(array) { init(array); };

  this.generateExample = function(id) {
    var initArr = []; // for id == 0 (empty)
    if (id == 1) { // (unbalanced BST example from Wikipedia)
      if (isAVL) {
        $('#create-err').html('AVL trees are balanced. Select the BST header to load this unbalanced BST test case.');
        setTimeout(function() {
          $('#create-err').html(""); // clear in 2s later
        }, 2000);
        return false;
      }
      initArr = [15,6,23,4,7,71,5,50];
    }
    else if (id == 2)
      initArr = [41,20,65,11,29,50,91,32,72,99];
    else if (id == 3)
      initArr = [16,8,24,4,12,20,28,2,6,10,14,18,22,26,30];
    else if (id == 4)
      initArr = [8,6,16,3,7,13,19,2,11,15,18,10];
    else if (id == 5)
      //initArr = [13,8,18,5,11,16,20,3,7,10,12,15,17,19,2,4,6,9,14,1];
      initArr = [13,8,18,5,16,11,20,3,15,10,19,7,17,12,14,2,6,9,4,1];
    init(initArr);
    return true;
  }

  this.generateRandom = function() {
    var vertexAmt = $("#N").val();
    var initArr = [];

    while (initArr.length < vertexAmt) { // still a set
      var random = Math.floor(1 + Math.random()*99); // [1..99]
      if ($.inArray(random, initArr) < 0) // distinct (some JavaScript error if I don't do this, despite now can do multiset from 27 May 2023 onwards
        initArr.push(random);
    }

    if (isAVL) {
      var initArrAvl = [];

      // note on 26 May 2023: this insertion strategy indeed creates an AVL tree, but not natural... (too balanced)
      // consider switching to really multiple insertions and rotations
      function recursion(startVal, endVal) {
        var total = startVal + endVal + 1;
        if (total < 1)
          return;
        if (startVal > endVal)
          return;
        if (total == 1)
          initArrAvl.push(initArr[startVal]);
        else if (total % 2 != 0) {
          initArrAvl.push(initArr[parseInt(total/2)]);
          recursion(startVal, parseInt(total/2) - 1);
          recursion(parseInt(total/2) + 1, endVal);
        }
        else {
          initArrAvl.push(initArr[parseInt(total/2) - 1]);
          recursion(startVal, parseInt(total/2) - 2);
          recursion(parseInt(total/2), endVal);
        }
      }

      function sortNumber(a, b) { return a-b; }
      initArr.sort(sortNumber);
      recursion(0, initArr.length-1);
      init(initArrAvl);
    }
    else {
      // 26 May 2023 version, see if it less biased than the previous one (too frequent that root has extreme smallest/largest)
      // https://javascript.info/task/shuffle
      function shuffle(array) {
        for (let i = array.length-1; i > 0; --i) {
          let j = Math.floor(Math.random() * (i+1));
          [array[i], array[j]] = [array[j], array[i]];
        }
      }
      shuffle(initArr);
      init(initArr);
    }

    return true;
  }

  this.generateSkewed = function(side) {
    if (isAVL) {
      $('#create-err').html('AVL trees are balanced. Select the BST header to load this unbalanced BST test case.');
      setTimeout(function() {
        $('#create-err').html('');
      }, 2000);
      return false;
    }
    else {
      var vertexAmt = Math.floor(6 + Math.random()*3); // [6..8] vertices (allow +1 for one more right/left extreme insertion)
      var initArr = new Array();
      while (initArr.length < vertexAmt) {
        var random = Math.floor(1 + Math.random()*99); // value [1..99]
        if ($.inArray(random, initArr) < 0)
          initArr.push(random);
      }
      if (side == "left") {
        initArr.sort(function(a, b) {
          return b-a;
        });
      }
      else if (side == "right") {
        initArr.sort(function(a, b) {
          return a-b;
        });
      }
      init(initArr);
      return true;
    }
  };

  this.search = function(v, mode, callback) {
    var sl = [], vertexTraversed = {}, edgeTraversed = {}, cur = iBST["root"], cs, currentVertexClass, key, ans;
    var lower_bound = 999, lb_key = null;
    v = parseInt(v);

    cs = createState(iBST);
    cs["status"] = 'The current BST rooted at {root}.'.replace('{root}', cur); // 'The current BST rooted at {root}'
    if (cur != null) // avoid empty tree case
      cs["vl"][iBST[cur]["vertexClassNumber"]]["extratext"] = "root";
    cs["lineNo"] = 0;
    sl.push(cs);

    var r = 0, prevRight = null;

    while (cur != v && cur != null) {
      var curLeft = iBST[cur]["leftChild"], curRight = iBST[cur]["rightChild"];
      var q = 0;
      if (curLeft != null) // has left child
        q = iBST[curLeft]["sz"];

      cs = createState(iBST, vertexTraversed, edgeTraversed);
      key = iBST[cur]["vertexClassNumber"];
      if (parseInt(cur) >= v) {
        if (parseInt(cur) < lower_bound) { // lower_bound is the smallest key in the traversal path of search(v) that is >= v
          lower_bound = parseInt(cur);
          lb_key = key;
        }
      }

      cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
      if (mode == 1) { // lower bound
        cs["vl"][key]["extratext"] = 'rank='+(r+q+1);
        if (prevRight != null)
          cs["vl"][prevRight]["extratext"] = 'rank='+r;
        if (curLeft != null)
          cs["vl"][curLeft]["extratext"] = "size="+q;
      }
      vertexTraversed[cur] = true;
      cs["status"] = 'Comparing  {cur} with {v}.'.replace("{cur}", cur).replace("{v}", v); // 'Comparing {cur} with {v}.'
      cs["lineNo"] = 3;
      sl.push(cs);

      if (v > parseInt(cur)) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        if (mode == 1) { // lower bound
          cs["vl"][key]["extratext"] = 'rank='+(r+q+1);
          if (prevRight != null)
            cs["vl"][prevRight]["extratext"] = 'rank='+r;
          if (curLeft != null)
            cs["vl"][curLeft]["extratext"] = "size="+q;
        }
        cs["status"] = '{cur} is smaller than {v}.'.replace("{cur}", cur).replace("{v}", v); // '{cur} is smaller than {v}.'
        cs["lineNo"] = 5;
        sl.push(cs);

        prevRight = cur;
        cur = iBST[cur]["rightChild"];
        r += (q+1); // all of these are beaten by v
        if (cur == null) break;

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        var edgeHighlighted = iBST[cur]["vertexClassNumber"];
        edgeTraversed[edgeHighlighted] = true;
        cs["el"][edgeHighlighted]["animateHighlighted"] = true;
        cs["el"][edgeHighlighted]["state"] = EDGE_TRAVERSED;
        cs["status"] = 'So search on the right.'; // 'So search on the right.'
        cs["lineNo"] = 6;
        sl.push(cs);
      }
      else {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        if (mode == 1) { // lower bound
          cs["vl"][key]["extratext"] = 'rank='+(r+q+1);
          if (prevRight != null)
            cs["vl"][prevRight]["extratext"] = 'rank='+r;
          if (curLeft != null)
            cs["vl"][curLeft]["extratext"] = "size="+q;
        }
        cs["status"] = '{cur} is greater than {v}.'.replace("{cur}", cur).replace("{v}", v); // '{cur} is greater than {v}.'
        cs["lineNo"] = 7;
        sl.push(cs);

        cur = iBST[cur]["leftChild"];
        if (cur == null) break;

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        var edgeHighlighted = iBST[cur]["vertexClassNumber"];
        edgeTraversed[edgeHighlighted] = true;
        cs["el"][edgeHighlighted]["animateHighlighted"] = true;
        cs["el"][edgeHighlighted]["state"] = EDGE_TRAVERSED;
        cs["status"] = 'So search on the left.'; // 'So search on the left.'
        cs["lineNo"] = 7;
        sl.push(cs);
      }
    }

    if (cur != null) {
      var curLeft = iBST[cur]["leftChild"], curRight = iBST[cur]["rightChild"];
      var q = 0;
      if (curLeft != null) // has left child
        q = iBST[curLeft]["sz"];

      cs = createState(iBST, vertexTraversed, edgeTraversed);
      key = iBST[cur]["vertexClassNumber"];
      cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
      if (mode == 1) { // only in lower bound mode for now
        cs["vl"][key]["extratext"] = 'v, rank='+(r+q+1);
        if (prevRight != null)
          cs["vl"][prevRight]["extratext"] = 'rank='+r;
        if (curLeft != null)
          cs["vl"][curLeft]["extratext"] = "size="+q;
      }
      cs["status"] = 'Value {v} is found.'.replace("{v}", v); // 'Value {v} is found.'
      cs["lineNo"] = 4;
      sl.push(cs);
    }
    else {
      if (mode == 0) { // exact
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["status"] = 'Value {v} is not in the BST.'.replace("{v}", v); // 'Value {v} is not in the BST.'
        cs["lineNo"] = [1, 2];
        sl.push(cs);
      }
      else if (mode == 1) { // lower bound
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        if (lb_key == null) {
          cs["status"] = 'Value {v} is not in the BST.'.replace("{v}", v) + '<br>There is no lower bound as {v} is greater than all keys in BST.'.replace('{v}', v); // 'Value {v} is not in the BST.'
          cs["lineNo"] = [1, 2];
        }
        else { // there is a lower bound
          cs["vl"][lb_key]["state"] = VERTEX_HIGHLIGHTED;
          cs["vl"][lb_key]["extratext"] = '^';
          cs["status"] = 'Value {v} is not in the BST.'.replace("{v}", v) + '<br>{lower_bound} is the lower bound of {v}.'.replace('{lower_bound}', lower_bound).replace('{v}', v); // 'Value {v} is not in the BST.'
          cs["lineNo"] = [1, 2];
        }
        sl.push(cs);
      }
    }

    gw.startAnimation(sl, callback);
    populatePseudocode(mode == 0 ? 3 : 4); // 3 for exact, 4 for lower bound
    return true;
  }

  this.findMax = function() { // special function so we can insert "one more than the biggest", etc
    var ans = -1;
    for (key in iBST) {
      if (key == "root") continue;
      ans = Math.max(ans, key);
    }
    return ans;
  }

  this.findMinMax = function(isMin, callback) {
    var sl = [], vertexTraversed = {}, edgeTraversed = {}, cur = iBST["root"], cs, key, ans;

    if (cur == null) { // special case checker
      cs = createState(iBST);
      if (isMin)
        cs["status"] = 'Tree is empty, there is no minimum value.'; // 'Tree is empty, there is no minimum value.'
      else
        cs["status"] = 'Tree is empty, there is no maximum value.'; // 'Tree is empty, there is no maximum value.'
      cs["lineNo"] = 1;
      sl.push(cs);
      populatePseudocode(isMin ? 1 : 2);
      gw.startAnimation(sl, callback);
      return true;
    }

    cs = createState(iBST);
    cs["status"] = 'The current BST rooted at {root}.'.replace('{root}', cur); // 'The current BST rooted at {root}'
    if (cur != null) // avoid empty tree case
      cs["vl"][iBST[cur]["vertexClassNumber"]]["extratext"] = "root";
    cs["lineNo"] = 0;
    sl.push(cs);

    while (cur != null) {
      cs = createState(iBST, vertexTraversed, edgeTraversed);
      key = iBST[cur]["vertexClassNumber"];
      cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
      cs["vl"][key]["extratext"] = '^';
      vertexTraversed[cur] = true;
      if (( isMin && (iBST[cur]["leftChild"] != null)) ||
          (!isMin && (iBST[cur]["rightChild"] != null))) {
        if (isMin)
          cs["status"] = '{cur} is not the minimum value as it has a left child.'.replace("{cur}", cur); // '{cur} is not the minimum value as it has a left child.'
        else
          cs["status"] = '{cur} is not the maximum value as it has a right child.'.replace("{cur}", cur); // '{cur} is not the maximum value as it has a right child.'
        cs["lineNo"] = 2;
      }
      else {
        ans = cur;
        if (isMin) {
          cs["status"] = 'Minimum value {val} found!'.replace('{val}', ans); // 'Minimum value {val} found!'
          cs["vl"][key]["extratext"] = "Min";
        }
        else {
          cs["status"] = 'Maximum value {val} found!'.replace('{val}', ans); // 'Maximum value {val} found!'
          cs["vl"][key]["extratext"] = "Max";
        }

        cs["lineNo"] = 4;
      }
      cur = (isMin ? iBST[cur]["leftChild"] : iBST[cur]["rightChild"]);
      sl.push(cs);

      if (cur == null) break;

      cs = createState(iBST, vertexTraversed, edgeTraversed);
      var edgeHighlighted = iBST[cur]["vertexClassNumber"];
      edgeTraversed[edgeHighlighted] = true;
      cs["el"][edgeHighlighted]["animateHighlighted"] = true;
      cs["el"][edgeHighlighted]["state"] = EDGE_TRAVERSED;
      if (isMin)
        cs["status"] = 'Go left to check for smaller value...'; // 'Go left to check for smaller value...'
      else
        cs["status"] = 'Go right to check for larger value...'; // 'Go right to check for larger value...'
      cs["lineNo"] = 3;
      sl.push(cs);
    }

    populatePseudocode(isMin ? 1 : 2);
    gw.startAnimation(sl, callback);
    return true;
  }

  this.insertArr = function(vertexTextArr, callback) {
    var sl = [], vertexTraversed = {}, edgeTraversed = {}, cur = iBST["root"], cs, key, currentVertexClass, i;

    cs = createState(iBST);
    cs["status"] = 'The current BST rooted at {root}.'.replace('{root}', cur); // 'The current BST rooted at {root}'
    if (cur != null) // avoid empty tree case
      cs["vl"][iBST[cur]["vertexClassNumber"]]["extratext"] = "root";
    cs["lineNo"] = 0;
    sl.push(cs);

    // Check whether input is array
    if (Object.prototype.toString.call(vertexTextArr) != '[object Array]') {
      $('#insert-err').html('Please fill in a number or comma-separated array of numbers!');
      return false;
    }

    // Loop through all array values and...
    var tempiBST = deepCopy(iBST); // Use this to simulate internal insertion

    for (i = 0; i < vertexTextArr.length; ++i) {
      var vt = parseInt(vertexTextArr[i]);

      // 1. Check whether value is number
      if (isNaN(vt)) {
        $('#insert-err').html('Please fill in a number or comma-separated array of numbers!');
        return false;
      }

      // 2. Check range
      if (parseInt(vt) < valueRange[0] || parseInt(vt) > valueRange[1]) {
        $('#insert-err').html('Sorry, only values between {range1} and {range2} can be inserted.'.replace("{range1}", valueRange[0]).replace("{range2}", valueRange[1]));
        return false;
      }

      // 26 May 2023, upgraded to multiset using freq attributes
      if (tempiBST[vt] != null)
        tempiBST[vt]["freq"] += 1; // add one more
      else {
        var parentVertex = parseInt(tempiBST["root"]);
        var heightCounter = 0;

        if (tempiBST["root"] == null) {
        // if (parentVertex == null) {
          tempiBST["root"] = parseInt(vt);
          tempiBST[vt] = {
            "parent": null,
            "leftChild": null,
            "rightChild": null,
            "freq": 1,
          };
        }
        else {
          while (true) {
            ++heightCounter;
            if (parentVertex < vt) {
              if (tempiBST[parentVertex]["rightChild"] == null)
                break;
              parentVertex = tempiBST[parentVertex]["rightChild"];
            }
            else {
              if (tempiBST[parentVertex]["leftChild"] == null)
                break;
              parentVertex = tempiBST[parentVertex]["leftChild"];
            }
          }

          if (parentVertex < vt)
            tempiBST[parentVertex]["rightChild"] = vt;
          else
            tempiBST[parentVertex]["leftChild"] = vt;

          tempiBST[vt] = {
            "parent": parentVertex,
            "leftChild": null,
            "rightChild": null,
            "freq": 1,
          }
        }

        ++heightCounter; // New vertex added will add new height
        if (heightCounter > maxHeightAllowed+1) {
          $('#insert-err').html('Sorry, this visualization can only support tree of maximum height {maxHeight}'.replace("{maxHeight}", maxHeightAllowed));
          if (typeof callback == 'function') callback();
          return false;
        }
      }
    }

    function checkNewHeight() {
      var parentVertex = tempiBST["root"];
      var heightCounter = 0;

      while (parentVertex != null) {
        if (parentVertex < parseInt(v))
          parentVertex = tempiBST[parentVertex]["rightChild"];
        else
          parentVertex = tempiBST[parentVertex]["leftChild"];
        ++heightCounter;
      }

      ++heightCounter; // New vertex added will add new height

      if (heightCounter > maxHeightAllowed+1)
        return false;
      return true;
    }

    for (i = 0; i < vertexTextArr.length; ++i) {
      var v = parseInt(vertexTextArr[i]);

      // Re-initialization
      vertexTraversed = {};
      edgeTraversed = {};
      cur = parseInt(iBST["root"]);
      cs = createState(iBST);

console.log("inserting " + v + ", cur = " + cur);

      // Find parent
      var need_new_vertex = true;
      while ((cur != null) && !isNaN(cur)) {
        //if (iBST["root"] == null) break;
        cs = createState(iBST, vertexTraversed, edgeTraversed);

console.log("now cur = " + cur);

        key = iBST[cur]["vertexClassNumber"];
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][key]["extratext"] = '^';
        vertexTraversed[cur] = true;
        cs["status"] = 'Comparing {v} with {cur}.'.replace("{v}", v).replace("{cur}", cur); // 'Comparing {v} with {cur}.'
        cs["lineNo"] = (!isAVL ? 3 : 1);
        sl.push(cs);

        var nextVertex;
        if (v > parseInt(cur))
          nextVertex = iBST[cur]["rightChild"];
        else if (v < parseInt(cur))
          nextVertex = iBST[cur]["leftChild"];
        else { // multiset
          iBST[cur]["freq"] += 1; // just increment this by one
          need_new_vertex = false;
          cs = createState(iBST, vertexTraversed, edgeTraversed);
          key = iBST[cur]["vertexClassNumber"];
          cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
          cs["vl"][key]["extratext"] = '^';
          cs["status"] = '{v} is equal to {cur}, so just increment its frequency.'.replace("{v}", v).replace("{cur}", cur); // '{v} is equal to {cur}, so just increment its frequency.'
          cs["lineNo"] = (!isAVL ? 7 : 1);
          sl.push(cs);
          break;
        }

        if (nextVertex == null)
          break;
        else
          cur = parseInt(nextVertex);

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        var edgeHighlighted = iBST[cur]["vertexClassNumber"];
        edgeTraversed[edgeHighlighted] = true;
        cs["el"][edgeHighlighted]["animateHighlighted"] = true;
        cs["el"][edgeHighlighted]["state"] = EDGE_TRAVERSED;
        if (v > parseInt(iBST[cur]["parent"])) {
          cs["status"] = '{v} is larger than {parent}, so go right.'.replace("{v}", v).replace("{parent}", iBST[cur]["parent"]); // '{v} is larger than {parent}, so go right.'
          cs["lineNo"] = (!isAVL ? 5 : 1);
        }
        else { // if (v < parseInt(iBST[cur]["parent"])) {
          cs["status"] = '{v} is smaller than {parent}, so go left.'.replace("{v}", v).replace("{parent}", iBST[cur]["parent"]); // '{v} is smaller than {parent}, so go left.'
          cs["lineNo"] = (!isAVL ? 4 : 1);
        }
        sl.push(cs);
      }

      if (!need_new_vertex) continue;

      // Begin insertion. First, update the internal representation
      iBST[v] = {
        "leftChild": null,
        "rightChild": null,
        "vertexClassNumber": v,
         "freq": 1,
      };

      if ((cur != null) && !isNaN(cur)) {
        iBST[v]["parent"] = cur;
        if (cur < v)
          iBST[cur]["rightChild"] = v;
        else
          iBST[cur]["leftChild"] = v;
      }
      else {
        iBST[v]["parent"] = null;
        iBST["root"] = v;
      }

      recalculatePosition();

      // Then, draw edge
      var newNodeVertexClass = iBST[v]["vertexClassNumber"];

      if ((cur != null) && !isNaN(cur)) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][newNodeVertexClass]["state"] = OBJ_HIDDEN;
        cs["el"][newNodeVertexClass]["state"] = EDGE_TRAVERSED;
        cs["el"][newNodeVertexClass]["animateHighlighted"] = true;
        cs["status"] = 'Location found!<br>Inserting {v}.'.replace("{v}", v); // 'Location found!<br>Inserting {v}.'
        cs["lineNo"] = 1;
        edgeTraversed[newNodeVertexClass] = true;
        sl.push(cs);
      }

      // Lastly, draw vertex
      cs = createState(iBST, vertexTraversed, edgeTraversed);
      cs["vl"][newNodeVertexClass]["state"] = VERTEX_HIGHLIGHTED; // EDGE_HIGHLIGHTED;
      cs["vl"][newNodeVertexClass]["extratext"] = "v";
      cs["status"] = '{v} has been inserted!'.replace("{v}", v); // '{v} has been inserted!'
      cs["lineNo"] = (!isAVL ? 2 : 1);
      sl.push(cs);

      if (isAVL) {
        recalculateBalanceFactor();

        var vertexCheckBf = iBST[v]["parent"];
        while (vertexCheckBf != null) {
          var vertexCheckBfClass = iBST[vertexCheckBf]["vertexClassNumber"];
          var bf = iBST[vertexCheckBf]["balanceFactor"];

          cs = createState(iBST);
          cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
          cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
          cs["status"] = 'Balance factor of {vertexCheckBf} is {bf}.<br>It is {status}.'.replace("{vertexCheckBf}", vertexCheckBf).replace("{bf}", bf).replace('{status}', (Math.abs(bf) <= 1 ? 'ok' : 'not ok')); // 'Balance factor of {vertexCheckBf} is {bf}.<br>It is {status}.'
          cs["lineNo"] = 2;
          sl.push(cs);

          if (bf == 2) {
            var vertexCheckBfLeft = iBST[vertexCheckBf]["leftChild"];
            var vertexCheckBfLeftClass = iBST[vertexCheckBfLeft]["vertexClassNumber"];
            var bfLeft = iBST[vertexCheckBfLeft]["balanceFactor"];

            cs = createState(iBST);
            cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
            cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
            cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
            cs["vl"][vertexCheckBfLeftClass]["extratext"] = "bf = " + bfLeft;
            cs["status"] = 'And balance factor of {vertexCheckBf} is {bf}.'.replace("{vertexCheckBf}", vertexCheckBfLeft).replace("{bf}", bfLeft); // 'And balance factor of {vertexCheckBf} is {bf}.'
            cs["lineNo"] = 2;
            sl.push(cs);

            if (bfLeft == 1 || bfLeft == 0) {
              rotateRight(vertexCheckBf);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfLeft)
                cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate right {vertexCheckBF}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate right {vertexCheckBf}.'
              cs["lineNo"] = 3;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfLeft)
                cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 3;
              sl.push(cs);
            }
            else if (bfLeft == -1) {
              var vertexCheckBfLeftRight = iBST[vertexCheckBfLeft]["rightChild"];
              var vertexCheckBfLeftRightClass = iBST[vertexCheckBfLeftRight]["vertexClassNumber"];

              rotateLeft(vertexCheckBfLeft);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate left {vertexCheckBf}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate left {vertexCheckBf}.'
              cs["lineNo"] = 4;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 4;
              sl.push(cs);

              rotateRight(vertexCheckBf);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfLeftRight)
                cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate right {vertexCheckBF}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate right {vertexCheckBf}.'
              cs["lineNo"] = 4;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfLeftRight)
                cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 4;
              sl.push(cs);
            }
          }
          else if (bf == -2) {
            var vertexCheckBfRight = iBST[vertexCheckBf]["rightChild"];
            var vertexCheckBfRightClass = iBST[vertexCheckBfRight]["vertexClassNumber"];
            var bfRight = iBST[vertexCheckBfRight]["balanceFactor"];

            cs = createState(iBST);
            cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
            cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
            cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
            cs["vl"][vertexCheckBfRightClass]["extratext"] = "bf = " + bfRight;
            cs["status"] = 'And balance factor of {vertexCheckBf} is {bf}.'.replace("{vertexCheckBf}", vertexCheckBfRight).replace("{bf}", bfRight); // 'And balance factor of {vertexCheckBf} is {bf}.'
            cs["lineNo"] = 2;
            sl.push(cs);

            if (bfRight == 1) {
              var vertexCheckBfRightLeft = iBST[vertexCheckBfRight]["leftChild"];
              var vertexCheckBfRightLeftClass = iBST[vertexCheckBfRightLeft]["vertexClassNumber"];

              rotateRight(vertexCheckBfRight);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate right {vertexCheckBF}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate right {vertexCheckBf}.'
              cs["lineNo"] = 6;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 6;
              sl.push(cs);

              rotateLeft(vertexCheckBf);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfRightLeft)
                cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate left {vertexCheckBf}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate left {vertexCheckBf}.'
              cs["lineNo"] = 6;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfRightLeft)
                cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 6;
              sl.push(cs);
            }
            else if (bfRight == -1 || bfRight == 0) {
              rotateLeft(vertexCheckBf);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfRight)
                cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate left {vertexCheckBf}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate left {vertexCheckBf}.'
              cs["lineNo"] = 5;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfRight)
                cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 5;
              sl.push(cs);
            }
          }

          if (vertexCheckBf != iBST["root"]) {
            cs = createState(iBST);
            cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
            cs["status"] = 'Check the parent vertex.'; // 'Check the parent vertex.'
            cs["lineNo"] = 2;
            sl.push(cs);
          }

          vertexCheckBf = iBST[vertexCheckBf]["parent"];
        }

        cs = createState(iBST);
        cs["status"] = 'The tree is balanced.'; // 'The tree is balanced.'
        cs["lineNo"] = 7;
        sl.push(cs);
      }
    }

    gw.startAnimation(sl, callback);
    populatePseudocode(isAVL ? 7 : 5); // 7 focus on rotation, 5 focus on insertion steps
    return true;
  }

  this.removeArr = function(vertexTextArr, callback) {
    var sl = [], vertexTraversed = {}, edgeTraversed = {}, cur = iBST["root"], cs, key, currentVertexClass, i;

    cs = createState(iBST);
    cs["status"] = 'The current BST rooted at {root}.'.replace('{root}', cur); // 'The current BST rooted at {root}'
    if (cur != null) // avoid empty tree case
      cs["vl"][iBST[cur]["vertexClassNumber"]]["extratext"] = "root";
    cs["lineNo"] = 0;
    sl.push(cs);

    if (Object.prototype.toString.call(vertexTextArr) != '[object Array]') {
      $('#remove-err').html('Please fill in a number or comma-separated array of numbers!');
      return false;
    }

    // Loop through all array values and...
    for (i = 0; i < vertexTextArr.length; ++i) {
      var vt = parseInt(vertexTextArr[i]);

      // Check whether value is number
      if (isNaN(vt)) {
        $('#remove-err').html('Please fill in a number or comma-separated array of numbers!');
        return false;
      }
      // Other checks not required
    }

    for (i = 0; i < vertexTextArr.length; ++i) {
      var v = parseInt(vertexTextArr[i]);
      var vertexCheckBf;

      // Re-initialization
      vertexTraversed = {};
      edgeTraversed = {};
      cur = iBST["root"];

      // Find vertex
      var need_to_delete = true;
      while (cur != null) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        key = iBST[cur]["vertexClassNumber"];
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][key]["extratext"] = '^';
        cs["status"] = 'Searching for vertex {v} to remove.'.replace("{v}", v); // 'Searching for vertex {v} to remove.'
        cs["lineNo"] = 1;
        sl.push(cs);

        if (v > parseInt(cur))
          cur = iBST[cur]["rightChild"];
        else if (v < parseInt(cur))
          cur = iBST[cur]["leftChild"];
        else { // multiset
          if (iBST[cur]["freq"] == 1) break; // do the actual deletion

          // frequency of cur is >= 2
          iBST[cur]["freq"] -= 1; // just decrement this by one
          need_to_delete = false;
          cs = createState(iBST, vertexTraversed, edgeTraversed);
          key = iBST[cur]["vertexClassNumber"];
          cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
          cs["vl"][key]["extratext"] = '^';
          cs["status"] = '{v} is equal to {cur}, so just decrement its frequency.'.replace("{v}", v).replace("{cur}", cur); // '{v} is equal to {cur}, so just decrement its frequency.'
          cs["lineNo"] = (!isAVL ? 2 : 1);
          sl.push(cs);
          break;
       }

        if (cur == null) break; // nothing to delete

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        var edgeHighlighted = iBST[cur]["vertexClassNumber"];
        edgeTraversed[edgeHighlighted] = true;
        cs["el"][edgeHighlighted]["animateHighlighted"] = true;
        cs["el"][edgeHighlighted]["state"] = EDGE_TRAVERSED;
        cs["status"] = 'Searching for vertex {v} to remove.'.replace("{v}", v); // 'Searching for vertex {v} to remove.'
        cs["lineNo"] = 1;
        sl.push(cs);
      }

      if (!need_to_delete) continue;

      if (cur != null) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        currentVertexClass = iBST[cur]["vertexClassNumber"];
        cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["status"] = 'Searching for vertex {v} to remove.'.replace("{v}", v); // 'Searching for vertex {v} to remove'
        cs["lineNo"] = 1;
        sl.push(cs);
      }
      else { // v is not in the BST
        cs = createState(iBST);
        cs["status"] = 'Vertex {v} is not in the BST.'.replace("{v}", v); // 'Vertex {v} is not in the BST.'
        cs["lineNo"] = 0;
        sl.push(cs);
        continue;
      }

      // Vertex found; begin deletion
      // Case 1: no child
      if (iBST[cur]["leftChild"] == null && iBST[cur]["rightChild"] == null) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][currentVertexClass]["extratext"] = 'Remove';
        cs["status"] = 'Vertex {v} has no children (a leaf).'.replace("{v}", v); // 'Vertex {v} has no children (a leaf).'
        cs["lineNo"] = (!isAVL ? 3 : 1);
        sl.push(cs);

        var parentVertex = iBST[cur]["parent"];

        if (parentVertex != null) {
          if (parseInt(parentVertex) < parseInt(cur))
            iBST[parentVertex]["rightChild"] = null;
          else
            iBST[parentVertex]["leftChild"] = null;
        }
        else
          iBST["root"] = null;

        currentVertexClass = iBST[cur]["vertexClassNumber"];
        delete iBST[cur];
        delete vertexTraversed[cur];
        delete edgeTraversed[currentVertexClass];

        recalculatePosition();

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["status"] = 'Remove leaf {v}.'.replace("{v}", v); // 'Remove leaf {v}.'
        cs["lineNo"] = (!isAVL ? 4 : 1);
        sl.push(cs);

        vertexCheckBf = parentVertex;
      }
      // Case 2: One child
      else if (iBST[cur]["leftChild"] == null) { // Only right child
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][currentVertexClass]["extratext"] = 'Remove';
        cs["status"] = 'Vertex {v} only has a right child.'.replace("{v}", v); // 'Vertex {v} only has a right child.'
        cs["lineNo"] = (!isAVL ? 5 : 1);
        sl.push(cs);

        var parentVertex = iBST[cur]["parent"];
        var rightChildVertex = iBST[cur]["rightChild"];

        if (parentVertex != null) {
          if (parseInt(parentVertex) < parseInt(cur))
            iBST[parentVertex]["rightChild"] = rightChildVertex;
          else
            iBST[parentVertex]["leftChild"] = rightChildVertex;
        }
        else
          iBST["root"] = rightChildVertex;

        iBST[rightChildVertex]["parent"] = parentVertex;

        currentVertexClass = iBST[cur]["vertexClassNumber"];
        rightChildVertexClass = iBST[rightChildVertex]["vertexClassNumber"];
        delete iBST[cur];
        delete vertexTraversed[cur];
        delete edgeTraversed[currentVertexClass];

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][rightChildVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        if (parentVertex != null)
          cs["el"][rightChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = 'Remove vertex {v} and connect its parent to its right child.'.replace("{v}", v); // 'Remove vertex {v} and connect its parent to its right child.'
        cs["lineNo"] = (!isAVL ? 6 : 1);
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][rightChildVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        if (parentVertex != null)
          cs["el"][rightChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = (!isAVL ? 6 : 1);
        sl.push(cs);

        vertexCheckBf = rightChildVertex;
      }
      else if (iBST[cur]["rightChild"] == null) { // Only left child
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][currentVertexClass]["extratext"] = 'Remove';
        cs["status"] = 'Vertex {v} only has a left child.'.replace("{v}", v); // 'Vertex {v} only has a left child.'
        cs["lineNo"] = (!isAVL ? 5 : 1);
        sl.push(cs);

        var parentVertex = iBST[cur]["parent"];
        var leftChildVertex = iBST[cur]["leftChild"];

        if (parentVertex != null) {
          if (parseInt(parentVertex) < parseInt(cur))
            iBST[parentVertex]["rightChild"] = leftChildVertex;
          else
            iBST[parentVertex]["leftChild"] = leftChildVertex;
        }
        else
          iBST["root"] = leftChildVertex;

        iBST[leftChildVertex]["parent"] = parentVertex;

        currentVertexClass = iBST[cur]["vertexClassNumber"];
        leftChildVertexClass = iBST[leftChildVertex]["vertexClassNumber"];
        delete iBST[cur];
        delete vertexTraversed[cur];
        delete edgeTraversed[currentVertexClass];

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][leftChildVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        if (parentVertex != null)
          cs["el"][leftChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = 'Remove vertex {v} and connect its parent to its left child.'.replace("{v}", v); // 'Remove vertex {v} and connect its parent to its left child.'
        cs["lineNo"] = (!isAVL ? 6 : 1);
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][leftChildVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        if (parentVertex != null)
          cs["el"][leftChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = (!isAVL ? 6 : 1);
        sl.push(cs);

        vertexCheckBf = leftChildVertex;
      }
      else { // Case 3: two children
        var parentVertex = iBST[cur]["parent"];
        var leftChildVertex = iBST[cur]["leftChild"];
        var rightChildVertex = iBST[cur]["rightChild"];
        var successorVertex = iBST[cur]["rightChild"];
        var successorVertexClass = iBST[successorVertex]["vertexClassNumber"];

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][currentVertexClass]["extratext"] = 'Remove';
        cs["el"][successorVertexClass]["state"] = EDGE_TRAVERSED;
        cs["el"][successorVertexClass]["animateHighlighted"] = true;
        cs["status"] = 'Finding successor of {v}.'.replace("{v}", v); // 'Finding successor of {v}.'
        cs["lineNo"] = (!isAVL ? 7 : 1);
        sl.push(cs);

        edgeTraversed[successorVertexClass] = true;
        vertexTraversed[successorVertex] = true;

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][successorVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["status"] = 'Finding successor of {v}.'.replace("{v}", v); // 'Finding successor of {v}.'
        cs["lineNo"] = (!isAVL ? 7 : 1);
        sl.push(cs);

        while (iBST[successorVertex]["leftChild"] != null) {
          successorVertex = iBST[successorVertex]["leftChild"];
          successorVertexClass = iBST[successorVertex]["vertexClassNumber"];

          cs = createState(iBST, vertexTraversed, edgeTraversed);
          cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
          cs["el"][successorVertexClass]["state"] = EDGE_TRAVERSED;
          cs["el"][successorVertexClass]["animateHighlighted"] = true;
          cs["status"] = 'Finding successor of {v}.'.replace("{v}", v); // 'Finding successor {v}.'
          cs["lineNo"] = (!isAVL ? 7 : 1);
          sl.push(cs);

          edgeTraversed[successorVertexClass] = true;
          vertexTraversed[successorVertex] = true;

          cs = createState(iBST, vertexTraversed, edgeTraversed);
          cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
          cs["vl"][successorVertexClass]["state"] = VERTEX_HIGHLIGHTED;
          cs["status"] = 'Finding successor of {v}.'.replace("{v}", v); // 'Finding successor of {v}.'
          cs["lineNo"] = (!isAVL ? 7 : 1);
          sl.push(cs);
        }

        var successorParentVertex = iBST[successorVertex]["parent"]
        var successorRightChildVertex = iBST[successorVertex]["rightChild"];

        // Update internal representation
        if (parentVertex != null) {
          if (parseInt(parentVertex) < parseInt(cur))
            iBST[parentVertex]["rightChild"] = successorVertex;
          else
            iBST[parentVertex]["leftChild"] = successorVertex;
        }
        else
          iBST["root"] = successorVertex;

        iBST[successorVertex]["parent"] = parentVertex;
        iBST[successorVertex]["leftChild"] = leftChildVertex;

        iBST[leftChildVertex]["parent"] = successorVertex;

        if (successorVertex != rightChildVertex) {
          iBST[successorVertex]["rightChild"] = rightChildVertex;
          iBST[rightChildVertex]["parent"] = successorVertex;

          if (successorRightChildVertex != null) {
            if (parseInt(successorParentVertex) < parseInt(successorVertex))
              iBST[successorParentVertex]["rightChild"] = successorRightChildVertex;
            else
              iBST[successorParentVertex]["leftChild"] = successorRightChildVertex;
            iBST[successorRightChildVertex]["parent"] = successorParentVertex;
          }
          else {
            if (parseInt(successorParentVertex) < parseInt(successorVertex))
              iBST[successorParentVertex]["rightChild"] = null;
            else
              iBST[successorParentVertex]["leftChild"] = null;
          }
        }

        delete iBST[cur];
        delete vertexTraversed[cur];
        delete edgeTraversed[currentVertexClass];

        if (parentVertex == null)
          delete edgeTraversed[successorVertexClass];

//console.log(iBST["root"] + " " + successorVertex + "   " + iBST[iBST["root"]]["leftChild"] + " " + iBST[iBST["root"]]["rightChild"]);
        calcSize(iBST["root"]); // update all heights first to avoid N glitches to a small number
//console.log(iBST[iBST["root"]]["sz"]);

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        var leftChildVertexClass = iBST[leftChildVertex]["vertexClassNumber"];
        cs["vl"][successorVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][leftChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
        if (parentVertex != null) {
          var parentVertexClass = iBST[parentVertex]["vertexClassNumber"];
          cs["el"][successorVertexClass]["state"] = EDGE_HIGHLIGHTED;
        }
        if (successorVertex != rightChildVertex) {
          var rightChildVertexClass = iBST[rightChildVertex]["vertexClassNumber"];
          cs["el"][rightChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
          if (successorRightChildVertex != null) {
            var successorRightChildVertexClass = iBST[successorRightChildVertex]["vertexClassNumber"];
            cs["el"][successorRightChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
          }
        }
        cs["status"] = 'Replace vertex {v} with its successor.'.replace("{v}", v); // 'Replace vertex {v} with its successor.'
        cs["lineNo"] = (!isAVL ? 7 : 1);
        sl.push(cs);

        recalculatePosition();

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        leftChildVertexClass = iBST[leftChildVertex]["vertexClassNumber"];
        cs["vl"][successorVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        cs["el"][leftChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
        if (parentVertex != null) {
          var parentVertexClass = iBST[parentVertex]["vertexClassNumber"];
          cs["el"][successorVertexClass]["state"] = EDGE_HIGHLIGHTED;
        }
        if (successorVertex != rightChildVertex) {
          var rightChildVertexClass = iBST[rightChildVertex]["vertexClassNumber"];
          cs["el"][rightChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
          if (successorRightChildVertex != null) {
            var successorRightChildVertexClass = iBST[successorRightChildVertex]["vertexClassNumber"];
            cs["el"][successorRightChildVertexClass]["state"] = EDGE_HIGHLIGHTED;
          }
        }
        cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
        cs["lineNo"] = (!isAVL ? 7 : 1);
        sl.push(cs);

        vertexCheckBf = successorVertex;
        if (successorVertex != rightChildVertex)
          vertexCheckBf = successorParentVertex;
      }

      cs = createState(iBST);
      cs["status"] = 'Removal of {v} is complete.'.replace("{v}", v); // 'Removal of {v} is complete.'
      cs["lineNo"] = (!isAVL ? 0 : 1);
      sl.push(cs);

      if (isAVL) {
        recalculateBalanceFactor();

        while (vertexCheckBf != null) {
          var vertexCheckBfClass = iBST[vertexCheckBf]["vertexClassNumber"];

          var bf = iBST[vertexCheckBf]["balanceFactor"];

          cs = createState(iBST);
          cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
          cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
          cs["status"] = 'Balance factor of {vertexCheckBf} is {bf}.<br>It is {status}.'.replace("{vertexCheckBf}", vertexCheckBf).replace("{bf}", bf).replace('{status}', (Math.abs(bf) <= 1 ? 'ok' : 'not ok')); // 'Balance factor of {vertexCheckBf} is {bf}.<br>It is {status}.'
          cs["lineNo"] = 2;
          sl.push(cs);

          if (bf == 2) {
            var vertexCheckBfLeft = iBST[vertexCheckBf]["leftChild"];
            var vertexCheckBfLeftClass = iBST[vertexCheckBfLeft]["vertexClassNumber"];
            var bfLeft = iBST[vertexCheckBfLeft]["balanceFactor"];

            cs = createState(iBST);
            cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
            cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
            cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
            cs["vl"][vertexCheckBfLeftClass]["extratext"] = "bf = " + bfLeft;
            cs["status"] = 'And balance factor of {vertexCheckBf} is {bf}.'.replace("{vertexCheckBf}", vertexCheckBfLeft).replace("{bf}", bfLeft); // 'And balance factor of {vertexCheckBf} is {bf}.'
            cs["lineNo"] = 2;
            sl.push(cs);

            if (bfLeft == 1 || bfLeft == 0) {
              rotateRight(vertexCheckBf);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfLeft)
                cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate right {vertexCheckBF}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate right {vertexCheckBf}.'
              cs["lineNo"] = 3;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfLeft)
                cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 3;
              sl.push(cs);
            }
            else if (bfLeft == -1) {
              var vertexCheckBfLeftRight = iBST[vertexCheckBfLeft]["rightChild"];
              var vertexCheckBfLeftRightClass = iBST[vertexCheckBfLeftRight]["vertexClassNumber"];

              rotateLeft(vertexCheckBfLeft);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate left {vertexCheckBf}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate left {vertexCheckBf}.'
              cs["lineNo"] = 4;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 4;
              sl.push(cs);

              rotateRight(vertexCheckBf);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfLeftRight)
                cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate right {vertexCheckBF}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate right {vertexCheckBf}.'
              cs["lineNo"] = 4;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfLeftRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfLeftRight)
                cs["el"][vertexCheckBfLeftRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 4;
              sl.push(cs);
            }
          }
          else if (bf == -2) {
            var vertexCheckBfRight = iBST[vertexCheckBf]["rightChild"];
            var vertexCheckBfRightClass = iBST[vertexCheckBfRight]["vertexClassNumber"];
            var bfRight = iBST[vertexCheckBfRight]["balanceFactor"];

            cs = createState(iBST);
            cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
            cs["vl"][vertexCheckBfClass]["extratext"] = "bf = " + bf;
            cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
            cs["vl"][vertexCheckBfRightClass]["extratext"] = "bf = " + bfRight;
            cs["status"] = 'And balance factor of {vertexCheckBf} is {bf}.'.replace("{vertexCheckBf}", vertexCheckBfRight).replace("{bf}", bfRight); // 'And balance factor of {vertexCheckBf} is {bf}.'
            cs["lineNo"] = 2;
            sl.push(cs);

            if (bfRight == 1) {
              var vertexCheckBfRightLeft = iBST[vertexCheckBfRight]["leftChild"];
              var vertexCheckBfRightLeftClass = iBST[vertexCheckBfRightLeft]["vertexClassNumber"];

              rotateRight(vertexCheckBfRight);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate right {vertexCheckBF}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate right {vertexCheckBf}.'
              cs["lineNo"] = 6;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 6;
              sl.push(cs);

              rotateLeft(vertexCheckBf);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfRightLeft)
                cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate left {vertexCheckBf}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate left {vertexCheckBf}.'
              cs["lineNo"] = 6;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightLeftClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfRightLeft)
                cs["el"][vertexCheckBfRightLeftClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 6;
              sl.push(cs);
            }
            else if (bfRight == -1 || bfRight == 0) {
              rotateLeft(vertexCheckBf);

              cs = createState(iBST);
              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfRight)
                cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Rotate left {vertexCheckBf}.'.replace("{vertexCheckBf}", vertexCheckBf); // 'Rotate left {vertexCheckBf}.'
              cs["lineNo"] = 5;
              sl.push(cs);

              recalculatePosition();

              cs = createState(iBST);

              cs["vl"][vertexCheckBfClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["vl"][vertexCheckBfRightClass]["state"] = VERTEX_HIGHLIGHTED;
              cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
              if (iBST["root"] != vertexCheckBfRight)
                cs["el"][vertexCheckBfRightClass]["state"] = EDGE_HIGHLIGHTED;
              cs["status"] = 'Relayout the BST and recompute its height.'; // 'Relayout the BST and recompute its height.'
              cs["lineNo"] = 5;
              sl.push(cs);
            }
          }

          if (vertexCheckBf != iBST["root"]) {
            cs = createState(iBST);
            cs["el"][vertexCheckBfClass]["state"] = EDGE_HIGHLIGHTED;
            //cs["status"] = "Check the parent vertex...";  //status_remove_17
            cs["status"] = 'Check the parent vertex...';
            cs["lineNo"] = 2;
            sl.push(cs);
          }

          vertexCheckBf = iBST[vertexCheckBf]["parent"];
        }

        cs = createState(iBST);
        cs["status"] = 'The tree is balanced.';
        cs["lineNo"] = 7;
        sl.push(cs);
      }
    }

    gw.startAnimation(sl, callback);
    populatePseudocode(isAVL ? 8 : 6);
    return true;
  };

  this.findPredSucc = function(v, isPred, callback) {
    var sl = [], vertexTraversed = {}, edgeTraversed = {}, cur = iBST["root"], cs, key, currentVertexClass;
    v = parseInt(v);

    if (v == null || v == undefined || isNaN(v)) {
      $('#predsucc-err').html('Please fill in a valid value!');
      return false;
    }

    if (iBST[v] == null) {
      $('#predsucc-err').html('Please fill in a value that is present inside the BST!');
      return false;
    }

    cs = createState(iBST);
    cs["status"] = 'The current BST rooted at {root}.'.replace('{root}', cur); // 'The current BST rooted at {root}'
    if (cur != null) // avoid empty tree case
      cs["vl"][iBST[cur]["vertexClassNumber"]]["extratext"] = "root";
    cs["lineNo"] = 0;
    sl.push(cs);

    cur = v;
    key = iBST[v]["vertexClassNumber"];
    if (( isPred && (iBST[v]["leftChild"] != null)) ||
        (!isPred && (iBST[v]["rightChild"] != null))) {
      var subTreeRoot = (isPred ? iBST[v]["leftChild"] : iBST[v]["rightChild"]);
      var subTreeRootKey = iBST[subTreeRoot]["vertexClassNumber"];

      edgeTraversed[subTreeRootKey] = true;

      cs = createState(iBST, vertexTraversed, edgeTraversed);
      cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
      cs["el"][subTreeRootKey]["animateHighlighted"] = true;
      if (isPred)
        cs["status"] = 'This vertex has a left child, so go left.'; // 'This vertex has a left child, so go left.'
      else
        cs["status"] = 'This vertex has a right child, so go right.'; // 'This vertex has a right child, so go right.'

      cs["lineNo"] = 1;
      sl.push(cs);

      cs = createState(iBST, vertexTraversed, edgeTraversed);
      cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
      cs["vl"][subTreeRootKey]["state"] = VERTEX_HIGHLIGHTED;
      if (isPred) {
        //cs["status"] = "Check whether the left child has a right child."; //status_predsucc_3
        cs["status"] = 'Check whether the left child has a right child.';
      } else {
        //cs["status"] = "Check whether the right child has a left child."; //status_predsucc_4
        cs["status"] = 'Check whether the right child has a left child.';
      }
      cs["lineNo"] = 1;
      sl.push(cs);

      if (( isPred && (iBST[subTreeRoot]["rightChild"] != null)) ||
          (!isPred && (iBST[subTreeRoot]["leftChild"] != null))) {
        cur = subTreeRoot;
        currentVertexClass = iBST[cur]["vertexClassNumber"];

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][subTreeRootKey]["state"] = VERTEX_HIGHLIGHTED;
        if (isPred) {
          //cs["status"] = "Right child found! Go to the right."; //status_predsucc_5
          cs["status"] = 'Right child found! Go to the right.';
        } else {
          //cs["status"] = "Left child found! Go to the left."; //status_predsucc_6
          cs["status"] = 'Left child found! Go to the left.';
        }
        cs["lineNo"] = 1;
        sl.push(cs);

        while (( isPred && (iBST[cur]["rightChild"] != null)) ||
               (!isPred && (iBST[cur]["leftChild"] != null))) {
          cs = createState(iBST, vertexTraversed, edgeTraversed);
          cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
          cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
          vertexTraversed[cur] = true;
          if (isPred) {
            //cs["status"] = cur + " is not the predecessor vertex as it has a right child."; //status_predsucc_7
            cs["status"] = '{cur} is not the predecessor vertex as it has a right child.'.replace("{cur}", cur);
          } else {
            //cs["status"] = cur + " is not the successor vertex as it has a left child.";  //status_predsucc_8
            cs["status"] = '{cur} is not the successor vertex as it has a left child.'.replace("{cur}", cur);
          }
          cs["lineNo"] = 1;
          sl.push(cs);

          cur = (isPred ? iBST[cur]["rightChild"] : iBST[cur]["leftChild"]);
          currentVertexClass = iBST[cur]["vertexClassNumber"];

          cs = createState(iBST, vertexTraversed, edgeTraversed);
          var edgeHighlighted = currentVertexClass;
          edgeTraversed[edgeHighlighted] = true;
          cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
          cs["el"][edgeHighlighted]["animateHighlighted"] = true;
          cs["el"][edgeHighlighted]["state"] = EDGE_TRAVERSED;
          if (isPred) {
            //cs["status"] = "Go right to check for larger value."; //status_predsucc_9
            cs["status"] = 'Go right to check for larger value.';
          } else {
            //cs["status"] = "Go left to check for smaller value."; //status_predsucc_10
            cs["status"] = 'Go left to check for smaller value.';
          }
          cs["lineNo"] = 1;
          sl.push(cs);
        }

        ans = cur;

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        if (isPred)
          cs["status"] = 'Predecessor found!<br>The predecessor of {v} is {ans}.'.replace("{v}", v).replace("{ans}", ans); // 'Predecessor found!<br>The predecessor of {v} is {ans}.'
        else
          cs["status"] = 'Successor found!<br>The successor of {v} is {ans}.'.replace("{v}", v).replace("{ans}", ans); // 'Successor found!<br>The successor of {v} is {ans}.'
        cs["vl"][key]["extratext"] = "v";
        cs["vl"][currentVertexClass]["extratext"] = (isPred ? "predecessor" : "successor") + " of v";
        cs["lineNo"] = 1;
        sl.push(cs);
      }
      else {
        ans = subTreeRoot;

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][subTreeRootKey]["state"] = VERTEX_HIGHLIGHTED;
        if (isPred)
          cs["status"] = 'No right child found, so this vertex is the predecessor.<br>The predecessor of {v} is {ans}.'.replace("{v}", v).replace("{ans}", ans); // 'No right child found, so this vertex is the predecessor.<br>The predecessor of {v} is {ans}.'
        else
          cs["status"] = 'No left child found, so this vertex is the successor.<br>The successor of {v} is {ans}.'.replace("{v}", v).replace("{ans}", ans); // 'No left child found, so this vertex is the successor.<br>The successor of {v} is {ans}.'
        cs["vl"][key]["extratext"] = "v";
        cs["vl"][subTreeRootKey]["extratext"] = (isPred ? "predecessor" : "successor") + " of v";
        cs["lineNo"] = 1;
        sl.push(cs);
      }
    }
    else {
      currentVertexClass = iBST[cur]["vertexClassNumber"];

      edgeTraversed[currentVertexClass] = true;

      cs = createState(iBST, vertexTraversed, edgeTraversed);
      cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
      cs["el"][currentVertexClass]["state"] = EDGE_HIGHLIGHTED;
      if (isPred)
        cs["status"] = 'No left child found, so check the parent.'; // 'No left child found, so check the parent.'
      else
        cs["status"] = 'No right child found, so check the parent.'; // 'No right child found, so check the parent.'
      cs["lineNo"] = [2, 3];
      sl.push(cs);

      cur = iBST[cur]["parent"];
      currentVertexClass = iBST[cur]["vertexClassNumber"];

      while (true) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        cs["vl"][currentVertexClass]["state"] = VERTEX_HIGHLIGHTED;
        vertexTraversed[cur] = true;
        if (( isPred && (cur > v)) ||
            (!isPred && (cur < v))) {
          if (isPred)
            cs["status"] = '{cur} is not the predecessor vertex as {v} is part of the left sub-tree.'.replace("{cur}", cur).replace("{v}", v); // '{cur} is not the predecessor vertex as {v} is part of the left sub-tree.'
          else
            cs["status"] = '{cur} is not the successor vertex as {v} is part of the right sub-tree.'.replace("{cur}", cur).replace("{v}", v); // '{cur} is not the successor vertex as {v} is part of the right sub-tree.'
          cs["lineNo"] = 4;
          sl.push(cs);
        }
        else {
          ans = cur;
          if (isPred)
            cs["status"] = 'Predecessor found!<br>The predecessor of {v} is {ans}.'.replace("{v}", v).replace("{ans}", ans); // 'Predecessor found!<br>The predecessor of {v} is {ans}.'
          else
            cs["status"] = 'Successor found!<br>The successor of {v} is {ans}.'.replace("{v}", v).replace("{ans}", ans); // 'Successor found!<br>The successor of {v} is {ans}.';
          cs["vl"][key]["extratext"] = "v";
          cs["vl"][currentVertexClass]["extratext"] = (isPred ? "predecessor" : "successor") + " of v";
          cs["lineNo"] = 7;
          sl.push(cs);
          break;
        }

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        var edgeHighlighted = currentVertexClass;
        if (cur != iBST["root"])
          edgeTraversed[edgeHighlighted] = true;
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        if (cur != iBST["root"])
          cs["el"][edgeHighlighted]["state"] = EDGE_HIGHLIGHTED;
        cs["status"] = 'Go up to check for smaller value.'; // 'Go up to check for smaller value.'
        cs["lineNo"] = 5;
        sl.push(cs);

        cur = iBST[cur]["parent"];
        if (cur == null) break;

        currentVertexClass = iBST[cur]["vertexClassNumber"];
      }

      if (cur == null) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
        if (isPred)
          cs["status"] = 'Parent is null, so {v} has no predecessor.'.replace("{v}", v); // 'Parent is null, so {v} has no predecessor.'
        else
          cs["status"] = 'Parent is null, so {v} has no successor.'.replace("{v}", v); // 'Parent is null, so {v} has no successor.'
        cs["lineNo"] = 6;
        sl.push(cs);

        ans = null;
      }
    }

    gw.startAnimation(sl, callback);
    populatePseudocode(isPred ? 9 : 10); // 9 for predecessor, 10 for successor
    return true;
  }

  this.select = function(k, callback) {
    var sl = [], vertexTraversed = {}, edgeTraversed = {}, cur = iBST["root"], cs, key;

    if (iBST["root"] == null) {
      cs = createState(iBST);
      cs["status"] = 'The Binary Search Tree is empty.<br>Return empty result.'; // 'The Binary Search Tree is empty.<br>Return empty result.';
      cs["lineNo"] = [1, 2];
      sl.push(cs);
      return true;
    }

    k = parseInt(k);
    if ((k < 1) || (k > this.getN())) { // k must be in [1..N]
      $('#select-err').html('k must be inside [1..' + getN() + ']');
      return false;
    }

    var original_k = k;
    var r = 0, prevRight = null, prevRank = 0;

    do {
      var curLeft = iBST[cur]["leftChild"], curRight = iBST[cur]["rightChild"];
      var q = 0;
      if (curLeft != null) // has left child
        q = iBST[curLeft]["sz"];

      if (q+1 == k) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][cur]["state"] = VERTEX_TRAVERSED;
        cs["vl"][cur]["extratext"] = "rank="+(q+1);
        if (curLeft != null)
          cs["vl"][curLeft]["extratext"] = "size="+q;
        cs["status"] = 'Vertex {cur} has rank {q+1} in this subtree, it is == {k}.<br>This vertex is the {k}-th smallest on this subtree.'.replace("{cur}", cur).replace("{q+1}", q+1).replace("{k}", k).replace("{k}", k);
        cs["lineNo"] = 3;
        sl.push(cs);

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][cur]["state"] = VERTEX_TRAVERSED;
        cs["vl"][cur]["extratext"] = "original rank="+original_k;
        cs["status"] = 'This vertex is the {original_k}-th smallest in the whole BST.'.replace("{original_k}", original_k);
        cs["lineNo"] = 3;
        sl.push(cs);
        break;
      }
      else if (q+1 > k) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][cur]["state"] = VERTEX_TRAVERSED;
        cs["vl"][cur]["extratext"] = "rank="+(q+1);
//        if (prevRight != null)
//          cs["vl"][prevRight]["extratext"] = 'rank='+prevRank;
        if (curLeft != null)
          cs["vl"][curLeft]["extratext"] = "size="+q;
        cs["status"] = 'Vertex {cur} has rank {q+1} in this subtree, it is &gt; {k}.<br>Select the {k}-th smallest on the left subtree.'.replace("{cur}", cur).replace("{q+1}", q+1).replace("{k}", k).replace("{k}", k);
        cs["lineNo"] = 4;
        sl.push(cs);

        cur = curLeft;

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][cur]["state"] = VERTEX_TRAVERSED;
        cs["status"] = 'At subtree rooted at vertex {cur}, looking for the {k}-th smallest.'.replace("{cur}", cur).replace("{k}", k);
        cs["lineNo"] = 4;
        sl.push(cs);
      }
      else if (q+1 < k) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][cur]["state"] = VERTEX_TRAVERSED;
        cs["vl"][cur]["extratext"] = "rank="+(q+1);
//        if (prevRight != null)
//          cs["vl"][prevRight]["extratext"] = 'rank='+prevRank;
        if (curLeft != null)
          cs["vl"][curLeft]["extratext"] = "size="+q;
        cs["status"] = 'Vertex {cur} has rank {q+1} in this subtree, it is &lt; {k}.<br>Select the {k}-{q}-1 = {k-q-1}-th smallest on the right subtree.'.replace("{cur}", cur).replace("{q+1}", q+1).replace("{k}", k).replace("{k}", k).replace("{q}", q).replace("{k-q-1}", k-q-1);
        cs["lineNo"] = 5;
        sl.push(cs);

        prevRight = cur;
        prevRank = r+q+1;
        r += (q+1);
        cur = curRight;
        k -= (q+1);

        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["vl"][cur]["state"] = VERTEX_TRAVERSED;
        cs["status"] = 'At subtree rooted at vertex {cur}, looking for the {k}-th smallest.'.replace("{cur}", cur).replace("{k}", k);
        cs["lineNo"] = 5;
        sl.push(cs);
      }
    }
    while (true);

    gw.startAnimation(sl, callback);
    populatePseudocode(14);
    return true;
  }

  this.treeTraversal = function(mode, callback) { // mode = 0 (inorder), 1 (preorder), 2 (postorder)
    var sl = [], vertexTraversed = {}, edgeTraversed = {}, cur = iBST["root"], cs, key;
    var vertexHighlighted = {};
    var in_list = "";

    if (iBST["root"] == null) {
      cs = createState(iBST);
      // "The Binary Search Tree is empty.<br>Return empty result.";
      cs["status"] = 'The Binary Search Tree is empty.<br>Return empty result.';
      cs["lineNo"] = [1, 2];
      sl.push(cs);
      return true;
    }
    else {
      key = iBST[iBST["root"]]["vertexClassNumber"];

      cs = createState(iBST, vertexTraversed, edgeTraversed);
      cs["vl"][key]["state"] = VERTEX_TRAVERSED;
      cs["vl"][key]["extratext"] = "root";
      // "The root {root} is not null.";
      cs["status"] = 'The root {root} is not null.'.replace("{root}", iBST["root"]);
      cs["lineNo"] = 1;
      sl.push(cs);

      traversalRecursion(mode, iBST["root"]);
    }

    cs = createState(iBST, vertexTraversed, edgeTraversed);
    highlightVertex(key);
    cs["status"] = '{mode} traversal of the whole BST is complete.<br>Visitation sequence: {in_list}.'.replace("{mode}", (mode == 0 ? "Inorder" : (mode == 1 ? "Preorder" : "Postorder"))).replace("{cur}", cur).replace("{in_list}", limit(in_list.slice(0, -1), 45)); // '{mode} traversal of the whole BST is complete.<br>Visitation sequence: {in_list}.'
    cs["vl"][key]["extratext"] = "root";
    cs["lineNo"] = 0;
    sl.push(cs);

    gw.startAnimation(sl, callback);

    function limit(str = '', limit = 0) {
      if (str.length < limit) return str;
      return str.substring(0, limit) + '..';
    }

    function traversalRecursion(mode, cur) {
      var key = iBST[cur]["vertexClassNumber"], curLeft = iBST[cur]["leftChild"], curRight = iBST[cur]["rightChild"];
      vertexTraversed[cur] = true;

      if (mode == 1) { // Preorder, visit upfront
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        vertexHighlighted[key] = true;
        highlightVertex(key);
        for (var r = 0; r < iBST[cur]["freq"]; ++r)
          in_list = in_list + cur + ",";
        cs["status"] = 'Visit vertex with value {cur}.<br>Visitation sequence: {in_list}.'.replace("{cur}", cur).replace("{in_list}", limit(in_list.slice(0, -1), 45)); // 'Visit vertex with value {cur}.<br>Visitation sequence: {in_list}.'
        cs["lineNo"] = 3;
        sl.push(cs);
      }

      if (curLeft == null) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        highlightVertex(key);
        // "The left child of vertex with value {cur} is empty.<br>Return empty.";
        cs["status"] = 'The left child of vertex with value {cur} is empty.<br>Return empty.'.replace("{cur}", cur);
        cs["lineNo"] = [1, 2];
        sl.push(cs);
      }
      else {
        var curLeftClass = iBST[curLeft]["vertexClassNumber"];

        edgeTraversed[curLeftClass] = true;
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["el"][curLeftClass]["animateHighlighted"] = true;
        highlightVertex(key);
        // "The left child of vertex with value {cur} is {curLeft} (not null).<br>So recurse to the left child.";
        cs["status"] = 'The left child of vertex with value {cur} is {curLeft} (not null).<br>So recurse to the left child.'.replace("{cur}", cur).replace("{curLeft}", curLeft);
        cs["lineNo"] = mode == 0 ? 3 : (mode == 1 ? 4 : 3);
        sl.push(cs);

        traversalRecursion(mode, curLeft);
      }

      if (mode == 0) { // Inorder, visit in the middle
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        vertexHighlighted[key] = true;
        highlightVertex(key);
        for (var r = 0; r < iBST[cur]["freq"]; ++r)
          in_list = in_list + cur + ",";
        cs["status"] = 'Visit vertex with value {cur}.<br>Visitation sequence: {in_list}.'.replace("{cur}", cur).replace("{in_list}", limit(in_list.slice(0, -1), 45)); // 'Visit vertex with value {cur}.<br>Visitation sequence: {in_list}...'
        cs["lineNo"] = 4;
        sl.push(cs);
      }

      if (curRight == null) {
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        highlightVertex(key);
        // "The right child of vertex with value {cur} is empty.<br>Return empty.";
        cs["status"] = 'The right child of vertex with value {cur} is empty.<br>Return empty.'.replace("{cur}", cur);
        cs["lineNo"] = [1, 2];
        sl.push(cs);
      }
      else {
        var curRightClass = iBST[curRight]["vertexClassNumber"];

        edgeTraversed[curRightClass] = true;
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        cs["el"][curRightClass]["animateHighlighted"] = true;
        highlightVertex(key);
        // "The right child of vertex with value {cur} is {curRight} (not null).";
        cs["status"] = 'The right child of vertex with value {cur} is {curRight} (not null).<br>So recurse to the right child.'.replace("{cur}", cur).replace("{curRight}", curRight);
        cs["lineNo"] = mode == 0 ? 5 : (mode == 1 ? 5 : 4);
        sl.push(cs);

        traversalRecursion(mode, curRight);
      }

      if (mode == 2) { // Postorder, visit at the end
        cs = createState(iBST, vertexTraversed, edgeTraversed);
        vertexHighlighted[key] = true;
        highlightVertex(key);
        for (var r = 0; r < iBST[cur]["freq"]; ++r)
          in_list = in_list + cur + ",";
        cs["status"] = 'Visit vertex with value {cur}.<br>Visitation sequence: {in_list}.'.replace("{cur}", cur).replace("{in_list}", limit(in_list.slice(0, -1), 45)); // 'Visit vertex with value {cur}.<br>Visitation sequence: {in_list}...'
        cs["lineNo"] = 5;
        sl.push(cs);
      }

      cs = createState(iBST, vertexTraversed, edgeTraversed);
      if (cur != iBST["root"])
        cs["el"][key]["state"] = EDGE_HIGHLIGHTED;
      highlightVertex(key);
      cs["status"] = '{mode} traversal of {cur} is complete.'.replace("{mode}", (mode == 0 ? "Inorder" : (mode == 1 ? "Preorder" : "Postorder"))).replace("{cur}", cur); // '{mode} traversal of {cur} is complete.'
      cs["lineNo"] = 0;
      sl.push(cs);
    }

    function highlightVertex(curkey) {
      for (var key in vertexHighlighted) cs["vl"][key]["state"] = VERTEX_HIGHLIGHTED;
      for (var key in vertexHighlighted) cs["vl"][key]["extratext"] = "";
      cs["vl"][curkey]["extratext"] = '^';
    }

    if (mode == 0)
      populatePseudocode(11);
    else if (mode == 1)
      populatePseudocode(12);
    else if (mode == 2)
       populatePseudocode(13);
    return true;
  }

  // Pseudocode for rotateLeft:
  /*
   * BSTVertex rotateLeft(BSTVertex T) // pre-req: T.right != null
   * BSTVertex w = T.right
   * w.parent = T.parent
   * T.parent = w
   * T.right = w.left
   * if (w.left != null) w.left.parent = T
   * w.left = T
   * // Update the height of T and then w
   * return w
   */

  function rotateLeft(val) {
    // Refer to pseudocode

    var t = parseInt(val);
    var w = iBST[t]["rightChild"];

    iBST[w]["parent"] = iBST[t]["parent"];
    if (iBST[t]["parent"] != null) {
      if (iBST[t]["parent"] < t) {
        var tParent = iBST[t]["parent"];
        iBST[tParent]["rightChild"] = w;
      }
      else {
        var tParent = iBST[t]["parent"];
        iBST[tParent]["leftChild"] = w;
      }
    }

    iBST[t]["parent"] = w;
    iBST[t]["rightChild"] = iBST[w]["leftChild"];
    if (iBST[w]["leftChild"] != null)
      iBST[iBST[w]["leftChild"]]["parent"] = t;
    iBST[w]["leftChild"] = t;

    if (t == iBST["root"])
      iBST["root"] = w;

    recalculateBalanceFactor();
  }

  function rotateRight(val) {
    // Refer to pseudocode

    var t = parseInt(val);
    var w = iBST[t]["leftChild"];

    iBST[w]["parent"] = iBST[t]["parent"];
    if (iBST[t]["parent"] != null) {
      if (iBST[t]["parent"] < t) {
        var tParent = iBST[t]["parent"];
        iBST[tParent]["rightChild"] = w;
      }
      else {
        var tParent = iBST[t]["parent"];
        iBST[tParent]["leftChild"] = w;
      }
    }

    iBST[t]["parent"] = w;
    iBST[t]["leftChild"] = iBST[w]["rightChild"];
    if (iBST[w]["rightChild"] != null)
      iBST[iBST[w]["rightChild"]]["parent"] = t;
    iBST[w]["rightChild"] = t;

    if (t == iBST["root"])
      iBST["root"] = w;

    recalculateBalanceFactor();
  }

  /*
   * iBSTObject: a JS object with the same structure of iBST. This means the BST doen't have to be the BST stored in this class
   * vertexTraversed: JS object with the vertexes of the BST which are to be marked as traversed as the key
   * edgeTraversed: JS object with the edges of the BST which are to be marked as traversed as the key
   */

  function createState(iBSTObject, vertexTraversed, edgeTraversed) {
    if (vertexTraversed == null || vertexTraversed == undefined || !(vertexTraversed instanceof Object))
      vertexTraversed = {};
    if (edgeTraversed == null || edgeTraversed == undefined || !(edgeTraversed instanceof Object))
      edgeTraversed = {};

    var info_str = "N=0, h=0 (empty BST)";
    if (iBSTObject["root"] != null)
      info_str = "N=" + iBSTObject[iBSTObject["root"]]["sz"] + ", h=" + iBSTObject[iBSTObject["root"]]["height"];

    var s = {
      "vl": {},
      "el": {},
      "info": info_str,
    };

    var key;
    var vertexClass;

    // something may be inconsistent during remove (AVL?), generates mini D3 error..., hunt for that bug
    for (key in iBSTObject) {
      if (key == "root") continue;

      vertexClass = iBSTObject[key]["vertexClassNumber"]

      s["vl"][vertexClass] = {};
      s["vl"][vertexClass]["cx"] = iBSTObject[key]["cx"];
      s["vl"][vertexClass]["cy"] = iBSTObject[key]["cy"];
      s["vl"][vertexClass]["text"] = key + (iBSTObject[key]["freq"] == 1 ? "" : ("-" + iBSTObject[key]["freq"]));
      s["vl"][vertexClass]["state"] = VERTEX_DEFAULT;
//      s["vl"][vertexClass]["extratext"] = iBSTObject[key]["sz"]; // let's debug this

      if (iBSTObject[key]["parent"] == null) continue;

      parentChildEdgeId = iBSTObject[key]["vertexClassNumber"];

      s["el"][parentChildEdgeId] = {};
      s["el"][parentChildEdgeId]["vertexA"] = iBSTObject[iBSTObject[key]["parent"]]["vertexClassNumber"];
      s["el"][parentChildEdgeId]["vertexB"] = iBSTObject[key]["vertexClassNumber"];
      s["el"][parentChildEdgeId]["type"] = EDGE_TYPE_UDE;
      s["el"][parentChildEdgeId]["weight"] = 1;
      s["el"][parentChildEdgeId]["state"] = EDGE_DEFAULT;
      s["el"][parentChildEdgeId]["animateHighlighted"] = false;
    }

    for (key in vertexTraversed) {
      vertexClass = iBSTObject[key]["vertexClassNumber"];
      s["vl"][vertexClass]["state"] = VERTEX_TRAVERSED;
    }

    for (key in edgeTraversed)
      s["el"][key]["state"] = EDGE_TRAVERSED;

    return s;
  }

  function calcSize(cur) {
    if (cur == null) return 0;
    iBST[cur]["sz"] = 1 + calcSize(iBST[cur]["leftChild"]) + calcSize(iBST[cur]["rightChild"]);
    return iBST[cur]["sz"];
  }

  function recalculatePosition() {
    calcDepth(iBST["root"], 0);
    calcHeight(iBST["root"]);
    calcSize(iBST["root"]);
    updatePosition(iBST["root"], 0, 0);

    function calcDepth(cur, curDepth) { // from top-down
      if (cur == null) return;
      iBST[cur]["depth"] = curDepth;
      calcDepth(iBST[cur]["leftChild"], curDepth+1);
      calcDepth(iBST[cur]["rightChild"], curDepth+1);
    }

    function calcHeight(cur) { // from bottom-up
      if (cur == null) return -1;
      iBST[cur]["height"] = 1 + Math.max(calcHeight(iBST[cur]["leftChild"]), calcHeight(iBST[cur]["rightChild"]));
      return iBST[cur]["height"];
    }

    function updatePosition(cur, r, d) {
      if (cur == null) return;

      var curLeft = iBST[cur]["leftChild"]; //, curRight = iBST[cur]["rightChild"];
      var q = 0;
      if (curLeft != null) // has left child
        q = iBST[curLeft]["sz"];

      if (rankBasedLayout) {
console.log('rank based for ' + cur);
        iBST[cur]["cx"] = (r+q+1)*(MAIN_SVG_WIDTH-50)/self.getN(); // put this vertex at this rank (each rank is equidistant: MAIN_SVG_WIDTH/self.getN())
      }
      else { // old, since 2011-2023, exactly half
console.log('half-half for ' + cur);
        if (cur == iBST["root"])
          iBST[cur]["cx"] = MAIN_SVG_WIDTH/2;
        else {
          var xAxisOffset = MAIN_SVG_WIDTH/2; // 26 May 23, will touch a bit at the 5th leaf level... ok lah, MAIN_SVG_WIDTH = 1000 cannot be enlarged too much to keep the mobile design intact
          var parentVertex = iBST[cur]["parent"];
          for (var i = 0; i < iBST[cur]["depth"]; ++i)
            xAxisOffset /= 2;

          if (parseInt(cur) > parseInt(parentVertex))
            iBST[cur]["cx"] = iBST[parentVertex]["cx"]+xAxisOffset;
          else
            iBST[cur]["cx"] = iBST[parentVertex]["cx"]-xAxisOffset;
        }
      }

      iBST[cur]["cy"] = 25 + 34*d; // iBST[cur]["depth"]; // 25 May 23, change 25 + 40* to 25 + 34* to make it similar to /heap, and at this depth
      updatePosition(iBST[cur]["leftChild"], r, d+1);
      updatePosition(iBST[cur]["rightChild"], r+q+1, d+1);
    }
  }

  function recalculateBalanceFactor() {
    balanceFactorRecursion(iBST["root"]);

    function balanceFactorRecursion(val) {
      if (val == null) return -1;

      var balanceFactorHeightLeft = balanceFactorRecursion(iBST[val]["leftChild"]);
      var balanceFactorHeightRight = balanceFactorRecursion(iBST[val]["rightChild"]);

      iBST[val]["balanceFactorHeight"] = Math.max(balanceFactorHeightLeft, balanceFactorHeightRight) + 1;
      iBST[val]["balanceFactor"] = balanceFactorHeightLeft - balanceFactorHeightRight;

      return iBST[val]["balanceFactorHeight"];
    }
  }

  function populatePseudocode(act) {
    $('#code5').html('');
    $('#code6').html('');
    $('#code7').html('');
    switch (act) {
      case 1: // searchMin
      case 2: // searchMax
        $('#code1').html('if this is null return empty'); // 'if this is null return empty'
        if (act == 1) {
          $('#code2').html('if left != null'); // 'if left != null'
          $('#code3').html('&nbsp;&nbsp;go left'); // '&nbsp;&nbsp;go left'
        }
        else {
          $('#code2').html('if right != null'); // 'if right != null'
          $('#code3').html('&nbsp&nbspgo right'); // '&nbsp&nbspgo right'
        }
        $('#code4').html('else return this key'); // 'else return this key'
        break;
      case 3: // search
      case 4: // lower_bound
        $('#code1').html('if this == null'); // 'if this == null'
        if (act == 3)
          $('#code2').html('&nbsp;&nbsp;return null'); // '&nbsp;&nbsp;return null'
        else
          $('#code2').html('&nbsp;&nbsp;return lowest traversed value &ge; v'); // '&nbsp;&nbsp;return lowest traversed value &ge; v'
        $('#code3').html('else if this key == search value'); // 'else if this key == search value'
        $('#code4').html('&nbsp;&nbsp;return this'); // '&nbsp;&nbsp;return this'
        $('#code5').html('else if this key < search value'); // 'else if this key < search value'
        $('#code6').html('&nbsp;&nbsp;search right'); // '&nbsp;&nbsp;search right'
        $('#code7').html('else search left'); // 'else search left'
        break;
      case 5: // Insert
        $('#code1').html('if insertion point is found'); // 'if insertion point is found'
        $('#code2').html('&nbsp;&nbsp;create new vertex'); // '&nbsp;&nbsp;create new vertex'
        $('#code3').html('if value to be inserted &lt; this key'); // 'if value to be inserted < this key'
        $('#code4').html('&nbsp;&nbsp;go left'); // '&nbsp;&nbsp;go left'
        $('#code5').html('else if value to be inserted &gt; this key'); // 'else if value to be inserted > this key'
        $('#code6').html('&nbsp;&nbsp;go right'); // '&nbsp;&nbsp;go right'
        $('#code7').html('else increment frequency'); // 'else increment frequency'
        break;
      case 6: // remove
        $('#code1').html('search for v'); // 'search for v'
        $('#code2').html('if v&#39;s freq &gt; 1, decrement by 1'); // 'if v's freq &gt; 1, decrement by 1'
        $('#code3').html('else if v is a leaf'); // 'else if v is a leaf'
        $('#code4').html('&nbsp; remove leaf v'); // '&nbsp;&nbsp;remove leaf v'
        $('#code5').html('else if v has 1 child'); // 'else if v has 1 child'
        $('#code6').html('&nbsp; bypass v'); // '&nbsp;&nbsp;bypass v'
        $('#code7').html('else replace v with successor'); // 'else replace v with successor'
        break;
      case 7: // insert with rotations
      case 8: // remove with rotations
        if (act == 7) {
          //$('#code1').html('insert v'); //code_insert_avl_1
          $('#code1').html('insert v');
        } else {
          //$('#code1').html('remove v'); //code_remove_avl_1
          $('#code1').html('remove v');
        }
        //$('#code2').html('check balance factor of this and its children');  //code_avl_2
        $('#code2').html('check balance factor of this and its children');
        //$('#code3').html('&nbsp;&nbsp;case1: this.rotateRight');  //code_avl_3
        $('#code3').html('&nbsp;&nbsp;case1: this.rotateRight');
        //$('#code4').html('&nbsp;&nbsp;case2: this.left.rotateLeft, this.rotateRight');  //code_avl_4
        $('#code4').html('&nbsp;&nbsp;case2: this.left.rotateLeft, this.rotateRight');
        //$('#code5').html('&nbsp;&nbsp;case3: this.rotateLeft'); //code_avl_5
        $('#code5').html('&nbsp;&nbsp;case3: this.rotateLeft');
        //$('#code6').html('&nbsp;&nbsp;case4: this.right.rotateRight, this.rotateLeft'); //code_avl_6
        $('#code6').html('&nbsp;&nbsp;case4: this.right.rotateRight, this.rotateLeft');
        //$('#code7').html('&nbsp;&nbsp;this is balanced'); //code_avl_7
        $('#code7').html('&nbsp;&nbsp;this is balanced');
        break;
      case 9: // predecessor
      case 10: // successor
        if (act == 9)
          $('#code1').html('if this.left != null return findMax(this.left)'); // 'if this.left != null return findMax(this.left)'
        else
          $('#code1').html('if this.right != null return findMin(this.right)'); // 'if this.right != null return findMin(this.right)'
        $('#code2').html('else'); // 'else'
        $('#code3').html('&nbsp;&nbsp;p = this.parent, T = this'); // '&nbsp;&nbsp;p = this.parent, T = this'
        if (act == 9)
          $('#code4').html('&nbsp;&nbsp;while (p != null &amp;&amp; T == p.left)'); // '&nbsp;&nbsp;while (p != null && T == p.left)'
        else
          $('#code4').html('&nbsp;&nbsp;while (p != null &amp;&amp; T == p.right)'); // '&nbsp;&nbsp;while (p != null && T == p.right)'
        $('#code5').html('&nbsp;&nbsp;&nbsp;&nbsp;T = p, p = T.parent'); // '&nbsp;&nbsp;&nbsp;&nbsp;T = p, p = T.parent'
        $('#code6').html('&nbsp;&nbsp;if p is null return -1'); // '&nbsp;&nbsp;if p is null return -1'
        $('#code7').html('&nbsp;&nbsp;else return p'); // '&nbsp;&nbsp;else return p'
        break;
      case 11: // inorder traversal
      case 12: // preorder traversal
      case 13: // postorder traversal
        $('#code1').html('if this is null'); // 'if this is null'
        $('#code2').html('&nbsp;&nbsp;return'); // '&nbsp;&nbsp;return'
        if (act == 11) {
          $('#code3').html('{mode}(left)'.replace("{mode}", "Inorder")); // '{mode}(left)'
          $('#code4').html('visit this'); // 'visit this'
          $('#code5').html('{mode}(right)'.replace("{mode}", "Inorder")); // '{mode}(right)'
        }
        else if (act == 12) {
          $('#code3').html('visit this'); // visit this
          $('#code4').html('{mode}(left)'.replace("{mode}", "Preorder")); // '{mode}(left)'
          $('#code5').html('{mode}(right)'.replace("{mode}", "Preorder")); // '{mode}(right)'
        }
        else if (act == 13) {
          $('#code3').html('{mode}(left)'.replace("{mode}", "Postorder")); // '{mode}(left)'
          $('#code4').html('{mode}(right)'.replace("{mode}", "Postorder")); // '{mode}(right)'
          $('#code5').html('visit this'); // 'visit this'
        }
        break;
      case 14: // select
        $('#code1').html('if this is null, return');
        $('#code2').html('q = size of left subtree');
        $('#code3').html('if (q+1 == k) return this');
        $('#code4').html('else if (q+1 > k) select k on left');
        $('#code5').html('else if (q+1 < k) select (k-q-1) on right');
        break;
    }
  }
}



// BSTaction.js
var actionsWidth = 150;
var statusCodetraceWidth = 420;

// local
var bw, gw;

$(function() {
  $('#play').hide();
  bw = new BST();
  gw = bw.getGraphWidget();
  gw.setAnimationDuration(700 / speedVal); // patch on 17 Apr 23 by Steven to make playback speed works as intended upon page load, need to do this only after gw is defined...

  var bstMode = getQueryVariable("mode");
  if (bstMode.length > 0)
    $('#title-' + bstMode).click();
  else { // if not specified, we throw a 50-50 coin
    option = ['BST', 'AVL']
    $('#title-' + option[Math.floor(Math.random()*2)]).click();
  }

  var createBST = getQueryVariable("create");
  if (createBST.length > 0) {
    var newBST = createBST.split(",");
    bw.generate(newBST);
  }
  else { // if not specified, we randomize this
    $("#N").val(Math.floor(7 + Math.random()*17)); // [7..23] short one for default randomness, our limit is 99
    random();
  }

  $("#v-search").val(bw.getRandom(true)); // 100% an existing value upfront (first click)
  $("#v-insert").val(Math.floor(1 + Math.random()*99) + "," +  Math.floor(1 + Math.random()*99)); // two [1..99], to show comma-separated
  $("#v-remove").val(bw.getRandom(true) + "," + bw.getRandom(true)); // to show comma-separated
  $("#v-predsucc").val(bw.getRandom(true));
  $("#k-select").val(1 + Math.floor(Math.random()*bw.getN())); // [1..N]
});

function closeCreate() {
  closeAction('create');
}

function adjust_scale() {
  if (bw.getH() > 5) // borderline between [4..5]
    setMediumScale(true);
  else
    setDefaultScale(true);
}

// title changing
$('#title-BST').click(function() {
  if (isPlaying) stop();
  showActionsPanel();
  hideStatusPanel();
  hideCodetracePanel();
  $("#N").val(Math.floor(7 + Math.random()*17));
  $("#create-example-unbalanced").show();
  $("#create-skewed").show();
  bw.isAVL(false);
  adjust_scale();
});

$('#title-AVL').click(function() {
  if (isPlaying) stop();
  showActionsPanel();
  hideStatusPanel();
  hideCodetracePanel();
  $("#N").val(Math.floor(7 + Math.random()*17));
  $("#create-example-unbalanced").hide();
  $("#create-skewed").hide();
  bw.isAVL(true);
  adjust_scale();
});

function example(id) {
  if (isPlaying) stop();
  if (bw.generateExample(id)) { // not 100% the same as commonAction
    $('#progress-bar').slider("option", "max", 0);
    isPlaying = false;
  }
  adjust_scale();
}

function random() {
  if (isPlaying) stop();
  if (bw.generateRandom()) { // not 100% the same as commonAction
    $('#progress-bar').slider("option", "max", 0);
    isPlaying = false;
  }
  adjust_scale();
}

function skewed(side) {
  if (isPlaying) stop();
  if (bw.generateSkewed(side)) { // not 100% the same as commonAction
    $('#progress-bar').slider("option", "max", 0);
    isPlaying = false;
  }
  setMediumScale(true); // always
}

function findMinMax(isMin, callback) {
  if (isPlaying) stop();
  adjust_scale();
  commonAction(bw.findMinMax(isMin, callback), "Search(" + (isMin ? "Min" : "Max") + ")");
}

function searchVertex(mode = 0, callback) {
  if (isPlaying) stop();
  adjust_scale();
  var v = $('#v-search').val();
  commonAction(bw.search(v, mode, callback), (mode == 0 ? "Search(" : "lower_bound(") + v + ")");
  setTimeout(function() {
    if (Math.random() >= 0.5) $("#v-search").val(bw.getRandom(true)); // 50% an existing value
    else                      $("#v-search").val(bw.getRandom(false)); // 50% a NON existing value
  }, 500);
}

function insertVertex(callback) {
  if (isPlaying) stop();
  adjust_scale();
  var v = $('#v-insert').val();
  commonAction(bw.insertArr(v.split(","), callback), "Insert(" + v + ")");
  setTimeout(function() { $("#v-insert").val(Math.floor(1 + Math.random()*99)); }, 500); // randomized for next click, a NON existing value in BST
}

function removeVertex(callback) {
  if (isPlaying) stop();
  adjust_scale();
  var v = $('#v-remove').val();
  commonAction(bw.removeArr(v.split(","), callback), "Remove(" + v + ")");
  setTimeout(function() { $("#v-remove").val(bw.getRandom(true)); }, 500); // randomized for next click, an existing value in BST
}

function predsucc(isPred, callback) {
  if (isPlaying) stop();
  adjust_scale();
  var v = $('#v-predsucc').val();
  commonAction(bw.findPredSucc(v.split(","), isPred, callback), (isPred ? "Predecessor(" : "Successor(") + v + ")");
  setTimeout(function() { $("#v-predsucc").val(bw.getRandom(true)); }, 500);
}

function select(callback) {
  if (isPlaying) stop();
  adjust_scale();
  var k = $('#k-select').val();
  commonAction(bw.select(k, callback), "Select(" + k + ")");
  setTimeout(function() { $("#k-select").val(1 + Math.floor(Math.random()*bw.getN())); }, 500);
}

function traversal(mode, callback) {
  if (isPlaying) stop();
  adjust_scale();
  commonAction(bw.treeTraversal(mode, callback), (mode == 0 ? "Inorder Traversal" : (mode == 1 ? "Preorder Traversal" : "Postorder Traversal")));
}

// Implement these functions in each visualisation
var userGraph = {
  'vl': {},
  'el': {},
};

// This function will be called before entering E-Lecture Mode
function ENTER_LECTURE_MODE() {
  //if (bw) userGraph = bw.getGraph();
}

// This function will be called before returning to Explore Mode
function ENTER_EXPLORE_MODE() {
  //loadGraph(userGraph);
}

// Lecture action functions
function CUSTOM_ACTION(action, data, mode) {
  if (action == 'search') {
    hideSlide(function() {
      $('#v-search').val(data); // force
      searchVertex(0, showSlide);
    });
  }
  else if (action == 'findmin') {
    hideSlide(function() {
      findMinMax(true, showSlide);
    });
  }
  else if (action == 'findmax') {
    hideSlide(function() {
      findMinMax(false, showSlide);
    });
  }
  else if (action == 'successor') {
    hideSlide(function() {
      $('#v-predsucc').val(data); // force
      predsucc(false, showSlide);
    });
  }
  else if (action == 'successor_max') {
    hideSlide(function() {
      $('#v-predsucc').val(bw.findMax()); // force the max
      predsucc(false, showSlide);
    });
  }
  else if (action == 'predecessor') {
    hideSlide(function() {
      $('#v-predsucc').val(data); // force
      predsucc(true, showSlide);
    });
  }
  else if (action == 'inorder') {
    hideSlide(function() {
      traversal(0, showSlide);
    });
  }
  else if (action == 'insert') {
    hideSlide(function() {
      $('#v-insert').val(data); // force
      insertVertex(showSlide);
    });
  }
  else if (action == 'insert_max_plus_1') {
    hideSlide(function() {
      $('#v-insert').val(bw.findMax()+1); // force the max plus 1
      insertVertex(showSlide);
    });
  }
  else if (action == 'remove') {
    hideSlide(function() {
      $('#v-remove').val(data); // force
      removeVertex(showSlide);
    });
  }
  else if (action == 'remove_max') {
    hideSlide(function() {
      $('#v-remove').val(bw.findMax()); // force the max
      removeVertex(showSlide);
    });
  }
}
</script>
  <script defer src="https://static.cloudflareinsights.com/beacon.min.js/vcd15cbe7772f49c399c6a5babf22c1241717689176015" integrity="sha512-ZpsOmlRQV6y907TI0dKBHq9Md29nnaEIPlkf84rnaERnq6zvWvPUqr2ft8M1aS28oN72PdrCzSjY4U6VaAw1EQ==" data-cf-beacon='{"version":"2024.11.0","token":"8d8ca7699cc74e9f80bd61a62d3d16a5","r":1,"server_timing":{"name":{"cfCacheStatus":true,"cfEdge":true,"cfExtPri":true,"cfL4":true,"cfOrigin":true,"cfSpeedBrain":true},"location_startswith":null}}' crossorigin="anonymous"></script>
</body>
</html>

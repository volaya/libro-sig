/** Generated TOC
    Stuart Langridge, July 2007
    
    Generate a table of contents, based on headings in the page.
    
    To place the TOC on the page, add
    
    <div id="generated-toc"></div>
    
    to the page where you want the TOC to appear. If this element
    is not present, the TOC will not appear.
*/

const generated_toc = {
  generate: function() {
    // Identify our TOC element, and what it applies to
    let generateFrom = '2';
    const tocparent = document.getElementById('generated-toc');
    
    const topNode = document.getElementById('chapter');
    
    // add all levels of heading we're paying attention to to the
    // headings_to_treat dictionary, ready to be filled in later
    const headingsToTreat = {"h6":''};
    for (let i=5; i>= parseInt(generateFrom); i--) {
      headingsToTreat["h" + i] = '';
    }
    
    // get headings
    let nodes = topNode.all ? topNode.all : topNode.getElementsByTagName('*');
    
    // put all the headings we care about in headings
    const headings = [];
    for (let i=0; i<nodes.length;i++) {
      if (nodes[i].nodeName.toLowerCase() in headingsToTreat) {
        // if heading has class no-TOC, skip it
        if ((' ' + nodes[i].className + ' ').indexOf('no-TOC') != -1) {
          continue;
        }
        headings.push(nodes[i]);
      }
    }
    
    const b = document.createElement('b');
    b.appendChild(document.createTextNode("ÍNDICE DEL CAPÍTULO"));
    tocparent.appendChild(b);
    
    // make the basic elements of the TOC itself
    let curHeadLvl = "h" + generateFrom;
    let curListEl = document.createElement('ul');
    tocparent.appendChild(curListEl);
    
    for (let i=0; i<headings.length;i++) {
      let thisHeadEl = headings[i];
      let thisHeadLvl = thisHeadEl.nodeName.toLowerCase();
      
      // this heading is at a lower level than the last one
      while (thisHeadLvl > curHeadLvl) {
        let lastListItemEl = 0;
        for (let j=curListEl.childNodes.length-1; j>=0;j--) {
          if (curListEl.childNodes[j].nodeName.toLowerCase() == 'li') {
            lastListItemEl = curListEl.childNodes[j];
            break;
          }
        }
        if (!lastListItemEl) {
          lastListItemEl = document.createElement('li');
        }
        const newListEl = document.createElement('ul');
        lastListItemEl.appendChild(newListEl);
        curListEl.appendChild(lastListItemEl);
        curListEl = newListEl;
        curHeadLvl = 'h' + (parseInt(curHeadLvl.substr(1,1)) + 1);
      }
      
      while (thisHeadLvl < curHeadLvl) {
        curListEl = curListEl.parentNode.parentNode;
        curHeadLvl = 'h' + (parseInt(curHeadLvl.substr(1,1)) - 1);
      }
      
      // create a link to this heading, and add it to the TOC
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#' + thisHeadEl.id;
      a.appendChild(document.createTextNode(generated_toc.innerText(thisHeadEl)));
      li.appendChild(a);
      curListEl.appendChild(li);
    }
    
    // go through the TOC and find all LIs that are "empty"
    const alllis = tocparent.getElementsByTagName("li");
    for (let i=0; i<alllis.length; i++) {
      let foundlink = false;
      for (let j=0; j<alllis[i].childNodes.length; j++) {
        if (alllis[i].childNodes[j].nodeName.toLowerCase() == 'a') {
          foundlink = true;
        }
      }
      if (!foundlink) {
        alllis[i].className = "missing";
      } else {
        alllis[i].className = "notmissing";
      }
    }
  },
  
  innerText: function(el) {
    return el.innerText || el.textContent || el.innerHTML.replace(/<[^>]+>/g, '');
  },
  
  init: function() {
    if (generated_toc.initialized) return;
    generated_toc.initialized = true;
    generated_toc.generate();
  }
};

// Modern DOM ready detection
function domReady(callback) {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', callback);
  } else {
    callback();
  }
}

domReady(generated_toc.init);

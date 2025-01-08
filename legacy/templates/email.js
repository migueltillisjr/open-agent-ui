document.addEventListener("DOMContentLoaded", () => {
  const toolbarItems = document.querySelectorAll(".draggable");
  const canvas = document.getElementById("canvas");
  const fontSizeControl = document.getElementById("font-size");
  const fontColorControl = document.getElementById("font-color");
  const boldButton = document.getElementById("bold");
  const italicButton = document.getElementById("italic");
  const underlineButton = document.getElementById("underline");
  const bulletsButton = document.getElementById("bullets");

  let selectedElements = new Set();

  // Initialize Sortable.js on the canvas for drag-and-drop reordering
  new Sortable(canvas, {
    animation: 150,
    ghostClass: "sortable-placeholder",
    handle: ".component", // Allow dragging components themselves
  });

  // Initialize Sortable.js on the canvas for ordering
  new Sortable(canvas, {
    animation: 150, // Smooth animation during reordering
    ghostClass: 'sortable-ghost', // Class applied to the element being dragged
    onEnd: function (evt) {
      console.log('New order:', Array.from(canvas.children).map(child => child.dataset.component || child.tagName));
    }});
    
  toolbarItems.forEach((item) => {
    item.addEventListener("dragstart", (e) => {
      e.dataTransfer.setData("component", e.target.dataset.component);
    });
  });

  canvas.addEventListener("dragover", (e) => {
    e.preventDefault();
    canvas.classList.add("droppable-over");
  });

  canvas.addEventListener("dragleave", () => {
    canvas.classList.remove("droppable-over");
  });

  canvas.addEventListener("drop", (e) => {
    e.preventDefault();
    canvas.classList.remove("droppable-over");

    const componentType = e.dataTransfer.getData("component");
    if (componentType) {
      const component = createComponent(componentType);
      canvas.appendChild(component);
    }
  });

  function createComponent(type) {
    const element = document.createElement("div");
    element.classList.add("component");
    element.setAttribute("contenteditable", "true");
    element.draggable = true; // Enable native dragging

    switch (type) {
      case "text":
        element.textContent = "This is an editable text block.";
        element.classList.add("text-component");
        break;
      case "image":
        element.innerHTML =
          '<img src="https://via.placeholder.com/150" alt="Placeholder Image">';
        element.setAttribute("contenteditable", "false"); // Images are not editable
        break;
      case "button":
        element.innerHTML = '<button>Click Me</button>';
        element.setAttribute("contenteditable", "false"); // Buttons are not editable
        break;
      default:
        element.textContent = "Unknown component";
    }

    element.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleSelection(element, e.ctrlKey || e.metaKey);
    });

    return element;
  }

  function toggleSelection(element, multiSelect) {
    if (multiSelect) {
      if (selectedElements.has(element)) {
        return; // Ignore if already selected
      } else {
        element.classList.add("selected");
        selectedElements.add(element);
      }
    } else {
      // Clear existing selections
      selectedElements.forEach((el) => el.classList.remove("selected"));
      selectedElements.clear();

      // Add new selection
      element.classList.add("selected");
      selectedElements.add(element);
    }
  }

  // Apply font size to selected elements
  fontSizeControl.addEventListener("change", () => {
    selectedElements.forEach((el) => {
      el.style.fontSize = `${fontSizeControl.value}px`;
    });
  });

  // Apply font color to selected elements
  fontColorControl.addEventListener("input", () => {
    selectedElements.forEach((el) => {
      el.style.color = fontColorControl.value;
    });
  });

  // Toggle bold for selected elements
  boldButton.addEventListener("click", () => {
    selectedElements.forEach((el) => {
      el.style.fontWeight = el.style.fontWeight === "bold" ? "normal" : "bold";
    });
  });

  // Toggle italic for selected elements
  italicButton.addEventListener("click", () => {
    selectedElements.forEach((el) => {
      el.style.fontStyle = el.style.fontStyle === "italic" ? "normal" : "italic";
    });
  });

  // Toggle underline for selected elements
  underlineButton.addEventListener("click", () => {
    selectedElements.forEach((el) => {
      el.style.textDecoration =
        el.style.textDecoration === "underline" ? "none" : "underline";
    });
  });

  // Toggle bullets for selected elements
  bulletsButton.addEventListener("click", () => {
    selectedElements.forEach((el) => {
      if (el.tagName === "DIV" && !el.querySelector("ul")) {
        const ul = document.createElement("ul");
        const li = document.createElement("li");
        li.textContent = el.textContent;
        ul.appendChild(li);
        el.innerHTML = "";
        el.appendChild(ul);
      } else if (el.querySelector("ul")) {
        el.innerHTML = el.querySelector("ul").innerText;
      }
    });
  });

  // Deselect all when clicking outside components
  canvas.addEventListener("click", (e) => {
    if (e.target === canvas) {
      selectedElements.forEach((el) => el.classList.remove("selected"));
      selectedElements.clear();
    }
  });
});

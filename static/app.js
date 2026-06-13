const dropzone = document.querySelector("#dropzone");
const fileInput = document.querySelector("#fileInput");
const chooseButton = document.querySelector("#chooseButton");
const convertButton = document.querySelector("#convertButton");
const copyButton = document.querySelector("#copyButton");
const downloadButton = document.querySelector("#downloadButton");
const fileMeta = document.querySelector("#fileMeta");
const helperText = document.querySelector("#helperText");
const preview = document.querySelector("#preview code");
const previewTitle = document.querySelector("#previewTitle");
const statusPill = document.querySelector("#statusPill");

let selectedFile = null;
let latestMarkdown = "";
let latestDownloadName = "converted.md";

function setStatus(text, isError = false) {
  statusPill.textContent = text;
  statusPill.classList.toggle("is-error", isError);
}

function describeSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

function selectFile(file) {
  selectedFile = file;
  latestMarkdown = "";
  latestDownloadName = "converted.md";
  convertButton.disabled = !file;
  copyButton.disabled = true;
  downloadButton.disabled = true;

  if (!file) {
    fileMeta.innerHTML = "<span>No file selected</span>";
    preview.textContent = "Select a file and convert it to see Markdown here.";
    previewTitle.textContent = "Markdown preview";
    return;
  }

  fileMeta.innerHTML = `<strong>${file.name}</strong><span>${describeSize(file.size)}</span>`;
  preview.textContent = "Ready to convert.";
  previewTitle.textContent = "Markdown preview";
  helperText.textContent = "Conversion runs locally on this machine.";
  setStatus("Ready");
}

async function convertSelectedFile() {
  if (!selectedFile) return;

  const payload = new FormData();
  payload.append("file", selectedFile);

  convertButton.disabled = true;
  copyButton.disabled = true;
  downloadButton.disabled = true;
  preview.textContent = "Converting...";
  helperText.textContent = "MarkItDown is reading the file.";
  setStatus("Working");

  try {
    const response = await fetch("/api/convert", {
      method: "POST",
      body: payload,
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Conversion failed.");
    }

    latestMarkdown = data.markdown || "";
    latestDownloadName = data.downloadName || "converted.md";
    preview.textContent = latestMarkdown || "_MarkItDown returned an empty document._";
    previewTitle.textContent = data.sourceName ? `${data.sourceName} -> Markdown` : "Markdown preview";
    copyButton.disabled = !latestMarkdown;
    downloadButton.disabled = false;
    helperText.textContent = "Markdown is ready to copy or download.";
    setStatus("Converted");
  } catch (error) {
    latestMarkdown = "";
    preview.textContent = error.message;
    helperText.textContent = "Fix the issue above and try again.";
    setStatus("Needs attention", true);
  } finally {
    convertButton.disabled = false;
  }
}

async function copyMarkdown() {
  if (!latestMarkdown) return;
  await navigator.clipboard.writeText(latestMarkdown);
  setStatus("Copied");
}

function downloadMarkdown() {
  const blob = new Blob([latestMarkdown], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = latestDownloadName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  setStatus("Downloaded");
}

chooseButton.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", () => selectFile(fileInput.files[0]));
convertButton.addEventListener("click", convertSelectedFile);
copyButton.addEventListener("click", copyMarkdown);
downloadButton.addEventListener("click", downloadMarkdown);

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropzone.classList.add("is-dragging");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("is-dragging");
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropzone.classList.remove("is-dragging");
  const file = event.dataTransfer.files[0];
  fileInput.files = event.dataTransfer.files;
  selectFile(file);
});

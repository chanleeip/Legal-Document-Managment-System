var dropZone = document.getElementById('drop_zone');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false)
    document.body.addEventListener(eventName, preventDefaults, false)
})

    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false)
})

    // Unhighlight drop zone when item is no longer over it
    ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false)
})

// Handle dropped files
dropZone.addEventListener('drop', handleDrop, false)

function preventDefaults (e) {
    e.preventDefault()
    e.stopPropagation()
}

function highlight(e) {
    dropZone.classList.add('highlight')
}

function unhighlight(e) {
    dropZone.classList.remove('highlight')
}

function handleDrop(e) {
    var dt = e.dataTransfer
    var files = dt.files

    handleFiles(files)
}

function handleFiles(files) {
    files = [...files]
    files.forEach(uploadFile)
}

function uploadFile(file) {
    var url = 'https://example.com/upload' // replace with your own endpoint URL
    var formData = new FormData()

    formData.append('file', file)

    fetch(url, {
        method: 'POST',
        body: formData,
        onUploadProgress: function(progressEvent) {
            var percentCompleted = Math.round( (progressEvent.loaded * 100) / progressEvent.total )
            document.getElementById('progress_bar').value = percentCompleted
        }
    })
        .then(response => {
            console.log(response)
        })
        .catch(error => {
            console.error(error)
        })
}
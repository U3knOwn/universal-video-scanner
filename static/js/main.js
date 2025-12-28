function startManualScan() {
    const button = document.getElementById('scanButton');
    const loading = document.getElementById('loadingIndicator');
    const message = document.getElementById('message');
    
    // Disable button and show loading
    button.disabled = true;
    loading.classList.add('active');
    message.style.display = 'none';
    
    // Make AJAX request to scan endpoint
    fetch('/scan', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading
        loading.classList.remove('active');
        button.disabled = false;
        
        // Show message
        message.className = 'message';
        if (data.new_files > 0) {
            message.classList.add('success');
            message.textContent = `✓ Scan abgeschlossen! ${data.new_files} neue Datei(en) gefunden.`;
        } else {
            message.classList.add('info');
            message.textContent = 'ℹ Keine neuen Dateien gefunden.';
        }
        message.style.display = 'block';
        
        // Reload page if new files were found
        if (data.new_files > 0) {
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
    })
    .catch(error => {
        loading.classList.remove('active');
        button.disabled = false;
        message.className = 'message';
        message.style.display = 'block';
        message.textContent = '✗ Fehler beim Scannen: ' + error;
    });
}

function loadFileList() {
    fetch('/get_files')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const select = document.getElementById('fileSelect');
                // Clear existing options except first
                select.innerHTML = '<option value="">-- Datei auswählen --</option>';
                
                // Add files to dropdown
                data.files.forEach(file => {
                    const option = document.createElement('option');
                    option.value = file.path;
                    option.textContent = file.name + (file.scanned ? ' ✓' : '');
                    if (file.scanned) {
                        option.style.color = '#4ecca3';
                    }
                    select.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Error loading file list:', error);
        });
}

function scanSelectedFile() {
    const select = document.getElementById('fileSelect');
    const filePath = select.value;
    
    if (!filePath) {
        return;
    }
    
    const button = document.getElementById('scanFileButton');
    const loading = document.getElementById('loadingIndicator');
    const message = document.getElementById('message');
    
    // Disable button and show loading
    button.disabled = true;
    loading.classList.add('active');
    message.style.display = 'none';
    
    // Make AJAX request to scan specific file
    fetch('/scan_file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ file_path: filePath })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading
        loading.classList.remove('active');
        button.disabled = false;
        
        // Show message
        message.className = 'message';
        if (data.success) {
            message.classList.add('success');
            message.textContent = '✓ ' + data.message;
            
            // Reload file list and page
            loadFileList();
            setTimeout(() => {
                location.reload();
            }, 2000);
        } else {
            message.classList.add('info');
            message.textContent = 'ℹ ' + data.message;
        }
        message.style.display = 'block';
    })
    .catch(error => {
        loading.classList.remove('active');
        button.disabled = false;
        message.className = 'message';
        message.style.display = 'block';
        message.textContent = '✗ Fehler beim Scannen: ' + error;
    });
}

// Enable/disable scan file button based on selection
document.getElementById('fileSelect').addEventListener('change', function() {
    document.getElementById('scanFileButton').disabled = !this.value;
});

// Load file list on page load
loadFileList();

// Auto-refresh every configured interval to show new automatically scanned files
setTimeout(() => {
    location.reload();
}, window.AUTO_REFRESH_INTERVAL * 1000);

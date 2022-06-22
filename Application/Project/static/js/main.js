// const file = document.querySelector('#file');
// file.addEventListener('change', (e) => {
//   // Get the selected file
//   const [file] = e.target.files;
//   // Get the file name and size
//   const { name: fileName, size } = file;
//   // Convert size in bytes to kilo bytes
//   const fileSize = (size / 1000).toFixed(2);
//   // Set the text content
//   const fileNameAndSize = `${fileName} - ${fileSize}KB`;
//   document.querySelector('.file-name').textContent = fileNameAndSize;
// });

updateList = function() {
  var input = document.getElementById('file');
  var output = document.getElementById('fileList');

  output.innerHTML = '<ul>';
  for (var i = 0; i < input.files.length; ++i) {
    output.innerHTML += input.files.item(i).name;
  }
  output.innerHTML += '</ul>';
}
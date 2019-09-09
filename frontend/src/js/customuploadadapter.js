class CustomUploadAdapter {
  static get pluginName() {
    return "CustomUploadAdapter";
  }

  constructor(loader) {
    this.loader = loader;
  }

  upload() {
    return new Promise((resolve, reject) => {
      const reader = (this.reader = new window.FileReader());

      reader.addEventListener("load", () => {
        resolve({ default: reader.result });
      });

      reader.addEventListener("error", err => {
        reject(err);
      });

      reader.addEventListener("abort", err => {
        reject(err);
      });

      this.loader.file.then(file => {
        reader.readAsDataURL(file);
      });
    });
  }

  abort() {
    this.reader.abort();
  }
}

export default function CustomUploadAdapterPlugin(editor) {
  editor.plugins.get("FileRepository").createUploadAdapter = loader => {
    return new CustomUploadAdapter(loader);
  };
}

## Image Similarity

### This API compares two images, and returns the simailarity as percentage

#### ▶ Usage

#### < API key authorization >

![](./usage/auth.png)

#### < Invalid API key >

![](./usage/invalid.png)

#### < Image URL inputs >

![](./usage/compare.png)

#### < Showing result >

![](./usage/result.png)

#### ▶  Packages to install

```bash
pip install flask
```
```bash
pip install Pillow  (instead of PIL)
```


#### ▶ Run the command 

```bash
export FLASK_APP=main
```
```bash
flask run
```

#### ▶  Environment

- OS : Windows
- Language : Python 3.9.0
- Libraries :
  - Flask
  - Pillow
  - ImageHash

# <div align="center"> Easy-Blog </div>

## <div align="center">Directory</div>
- [Project Name](#project-name)
- [Project Introduction](#project-introduction)
- [Usage](#usage)
- [Supported System](#supported-system)

## Project Name
#### Easy-Blog

## Project Introduction
#### The Easy Blog project can quickly build and run a simple blog on the CentOS system(Other Linux distributions may be supported in the future.), using Vue for the frontend and Python for the backend.
> [!NOTE]
> At present, this project is only used to cope with university coursework, so there may be many shortcomings in its use. It is also not recommended to use it for formal blog purposes. Perhaps it will continue to be improved in the future.

## Usage
#### 1. Download the project
```
git clone https://github.com/buttfa/Easy-Blog.git ~/Easy-Blog
```
#### 2. Enter the project directory
```
cd ~/Easy-Blog
```

#### 3. Build the project
> [!CAUTION]
> This instruction can be used to build the environment required for Easy Blog using the eblog.by script, and we have tried our best to avoid any impact on the system environment. If you have extremely high requirements for the system environment, please personally check the script or manually build the environment required for Easy Blog.
```
python eblog.py build centos
```
#### 4. Run the project in development mode
```
python eblog.py run
```
#### 5. Destroy the project
```
python eblog.py destroy
```

## Supported System
|Build command|Supported System|
|:-|:-|
|python eblog.py build centos|CentOS-9-Stream-x64|
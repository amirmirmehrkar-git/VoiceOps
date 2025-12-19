# CodeRabbit CLI Installation for Windows

## روش نصب در Windows

### گزینه 1: استفاده از WSL (توصیه می‌شود)

CodeRabbit CLI برای Linux/Mac طراحی شده است. بهترین روش در Windows استفاده از WSL است:

#### نصب WSL:
```powershell
wsl --install
```

پس از نصب WSL و restart کردن سیستم:

```bash
# در WSL terminal
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
source ~/.bashrc
coderabbit --version
```

---

### گزینه 2: دانلود مستقیم (اگر باینری Windows موجود باشد)

```powershell
# دانلود آخرین نسخه
$version = "v0.6.5"
$url = "https://cli.coderabbit.ai/releases/$version/coderabbit-windows-x64.zip"
Invoke-WebRequest -Uri $url -OutFile "coderabbit.zip"

# Extract
Expand-Archive -Path "coderabbit.zip" -DestinationPath "coderabbit"

# اضافه کردن به PATH
$coderabbitPath = (Resolve-Path "coderabbit").Path
$env:Path += ";$coderabbitPath"
```

---

### گزینه 3: استفاده از npm (اگر موجود باشد)

```powershell
npm install -g @coderabbit/cli
```

---

## احراز هویت

پس از نصب:

```bash
coderabbit auth login
```

این دستور یک URL نمایش می‌دهد که باید در مرورگر باز کنید و وارد حساب کاربری شوید.

---

## استفاده در پروژه VoiceOps

پس از نصب، می‌توانید از CodeRabbit برای بررسی کد استفاده کنید:

```bash
# بررسی تغییرات
coderabbit review

# بررسی با خروجی ساده
coderabbit review --plain

# بررسی با خروجی کم (برای صرفه‌جویی در token)
coderabbit review --prompt-only
```

---

## مستندات

برای اطلاعات بیشتر:
- [CodeRabbit CLI Docs](https://docs.coderabbit.ai/cli)
- [WSL Installation Guide](https://docs.coderabbit.ai/cli/wsl-windows)

---

## نکته

اگر WSL ندارید و نمی‌خواهید نصب کنید، می‌توانید از CodeRabbit در GitHub Actions یا CI/CD pipeline استفاده کنید.


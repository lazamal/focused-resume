# 1. Base Image
FROM public.ecr.aws/lambda/python:3.12

# 2. System Dependencies (Never changes - Cached)
RUN dnf install -y \
    atk cups-libs gtk3 libXcomposite libXcursor libXdamage libXext \
    libXi libXrender libXtst pango alsa-lib \
    mesa-libgbm nss nss-tools && dnf clean all

# 3. Requirements (Changes rarely - Cached)
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# 4. Playwright Browsers (Huge - MUST BE CACHED)
# We move this ABOVE the code so it's not re-installed on code changes
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN python -m playwright install chromium
RUN chmod -R 775 /ms-playwright

# 5. Heavy ML Models (The 6.5-minute step - CACHED)
# By putting this in its own layer before the app code, 
# you only wait 6 minutes ONCE.
COPY models/skill-extractor/ ./models/skill-extractor/

# 6. Your Project Folders & App Code (Fastest changing - LAST)
# Now, adding a print() only triggers THIS step.
COPY new_backend/ ./new_backend/
COPY app.py .

# 7. Set the CMD
CMD [ "app.handler" ]
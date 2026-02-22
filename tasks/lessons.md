# Lessons Learned

## 1. GCP Secret Manager vs Local `.env`
- **Failure Pattern**: Trying to debug missing/expired API keys by updating the local `.env` file, but the Cloud Function continues returning "400 API key expired".
- **Correct Approach**: Check the `deploy.sh` script. If `--set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest"` is used, the deployment aggressively locks to the GCP Secret Manager, completely ignoring local `.env`. The fix is to update the key via the `gcloud secrets versions add` command or GCP Console, and then **re-deploy** to flush the memory cache of warm Cloud Function instances.

## 2. Gemini `google_search` Tool vs Native Dependencies
- **Failure Pattern**: Using `tools={"google_search_retrieval": {}}` or `tools={"google_search": {}}` in the Gemini `generate_content` payload running on older pip packages (e.g. `google-generativeai`). This throws `ValueError: Unknown field for FunctionDeclaration: google_search`.
- **Correct Approach**: Do not blindly inject search tools if the environment uses an outdated, deprecated Python SDK. Fall back to removing the `tools=` parameter entirely and strictly prompt the model to utilize its internal knowledge base / implicit search capabilities instead of risking dependency hell.

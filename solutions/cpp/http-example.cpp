#include <iostream>
#include <string>
#include <curl/curl.h>
#include <json/json.h>

using namespace std;

// Helper function to write the data to a string
size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

Json::Value get(std::string url) {
    CURL* curl = curl_easy_init();
    CURLcode res;
    std::string readBuffer;
    
    // Disable ssl verification
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
    
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        
    res = curl_easy_perform(curl);
        
    if(res != CURLE_OK) {
        std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        return "";
    }

    curl_easy_cleanup(curl);
    
    // Parse the response JSON to get the evolution chain URL
    Json::Value data;
    Json::CharReaderBuilder reader;
    std::istringstream s(readBuffer);
    std::string errs;
    
    if (!Json::parseFromStream(reader, s, &data, &errs)) {
        std::cerr << "Failed to parse JSON: " << errs << std::endl;
        return "";
    }

    return data;
}

int main() {
    Json::Value type = get("https://pokeapi.co/api/v2/type/water");
    std::cout << "name: " << type["name"] << std::endl;
    std::cout << "name: " << type["name"].asString() << std::endl;
    std::cout << "first move (name): " << type["moves"][0]["name"] << std::endl;
    std::cout << "first move (url): " << type["moves"][0]["url"] << std::endl;

    return 0;
}
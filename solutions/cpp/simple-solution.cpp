#include <iostream>
#include <string>
#include <curl/curl.h>
#include <json/json.h>
#include <list>

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

// Function to get the evolution chain URL
Json::Value getEvolutionData(const std::string& pokemon_name) {
    Json::Value species = get("https://pokeapi.co/api/v2/pokemon-species/" + pokemon_name);
    Json::Value evolution_data = get(species["evolution_chain"]["url"].asString());
    return evolution_data;
}

// Function to get evolutions from the evolution chain URL
std::list<string> getEvolutions(const Json::Value& evolution_data) {
    Json::Value chain = evolution_data["chain"];
    
    std::list<string> evolutions = {};
    
    while (chain != NULL) {
        
        std::string species_name = chain["species"]["name"].asString();
        
        // Add an element at the beginning
        evolutions.push_back(species_name);

        if (!chain["evolves_to"].empty()) {
            chain = chain["evolves_to"][0];
        } else {
            chain = NULL;
        }
    }
    
    return evolutions;
}

int main() {
    std::string pokemon_name = "eevee";
    
    // Get the evolution chain URL
    Json::Value evolution_data = getEvolutionData(pokemon_name);
    std::list<string> evolutions = getEvolutions(evolution_data);
    
    for (auto e : evolutions)
        std::cout << e << "\n";

    return 0;
}
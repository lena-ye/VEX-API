#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <string>

std::string load_info(const std::string& path) {
    std::ifstream file(path);
    std::string key;
    if (file && std::getline(file, key)) {
        return key;
    }
    throw std::runtime_error("Could not load info from file.");
}

int main() {

    

    // API setup
    std::string base_url = "https://www.robotevents.com/api/v2/teams";

    // Headers
    std::string api_key = load_info("api_key.txt"); // you want to save this file in the same directory as ./RobotEventsAPI.exe
    cpr::Header headers = {
        {"Authorization", "Bearer " + api_key},
        {"Accept", "application/json"}
    };

    // Parameters
    std::string team_number = load_info("team_number.txt"); // you want to save this file in the same directory as ./RobotEventsAPI.exe
    cpr::Parameters params = {
        {"number[]", team_number}
    };

    // Make GET request
    cpr::Response response = cpr::Get(cpr::Url{base_url}, headers, params);

    std::cout << "Status Code: " << response.status_code << std::endl;

    if (response.status_code == 200) {
        try {
            // Parse JSON
            nlohmann::json data = nlohmann::json::parse(response.text);

            // Get current executable path (C++17)
            std::filesystem::path current_path = std::filesystem::current_path();
            std::filesystem::path file_path = current_path / "teams_cpp.json";

            // Write to file
            std::ofstream file(file_path);
            if (file.is_open()) {
                file << data.dump(4);  // Pretty print with indent=4
                file.close();
                std::cout << "File saved to: " << file_path << std::endl;
            } else {
                std::cerr << "Failed to open file for writing." << std::endl;
            }

        } catch (const std::exception& e) {
            std::cerr << "JSON parsing or writing error: " << e.what() << std::endl;
        }

    } else {
        std::cerr << "Request failed.\nResponse text:\n" << response.text << std::endl;
    }

    return 0;
}

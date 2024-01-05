//
//  APIService.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/9/23.
//

import Foundation

struct APIService {
    
    let baseURL = "https://yvx6t8lrvg.execute-api.us-west-1.amazonaws.com/dev/api"
    

    func fetch<T: Decodable>(_ type: T.Type, url: URL?, completion: @escaping(Result<T, APIError>) -> Void) {
        guard let url = url else {
            let error = APIError.badURL
            completion(Result.failure(error))
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { (data, response, error) in
            
            if let error = error as? URLError {
                completion(Result.failure(APIError.url(error)))
            } else if let response = response as? HTTPURLResponse, !(200...299).contains(response.statusCode) {
                completion(Result.failure(APIError.badResponse(statusCode: response.statusCode)))
            } else if let data = data {
                let decoder = JSONDecoder()
                do {
                    let result = try decoder.decode(type, from: data)
                    completion(Result.success(result))
                } catch {
                    completion(Result.failure(APIError.parsing(error as? DecodingError)))
                }
            }
        }
        task.resume()
    }
 
    func fetchBlocks(for parkId: Int, completion: @escaping(Result<[Block], APIError>) -> Void){
        let urlStr = "\(baseURL)/block/park/\(parkId)"
        print(urlStr)
        let url = URL(string: urlStr)
        
        fetch([Block].self, url: url, completion: completion)
    }
    
    func fetchAllParks(completion: @escaping(Result<[Park], APIError>) -> Void){
        let url = URL(string: "\(baseURL)/park")
        fetch([Park].self, url: url, completion: completion)
    }
    
    func fetchScoutStatus(completion: @escaping(Result<ScoutStatus, APIError>) -> Void){
        let url = URL(string: "\(baseURL)/navigationstate")
        fetch(ScoutStatus.self, url: url, completion: completion)
    }

    func fetchNetworkStatus(completion: @escaping(Result<NetworkStatus, APIError>) -> Void){
        let url = URL(string: "\(baseURL)/connectivitystate")
        fetch(NetworkStatus.self, url: url, completion: completion)
    }

    func fetchFedsStatus(completion: @escaping(Result<FedsStatus, APIError>) -> Void){
        let url = URL(string: "\(baseURL)/fedsofflinemode")
        fetch(FedsStatus.self, url: url, completion: completion)
    }

}

//
//  APIError.swift
//  FedsMonitoringApp
//
//  Created by Jagdish Patel on 3/9/23.
//

import Foundation

enum APIError: Error, CustomStringConvertible {
    case badURL
    case badResponse(statusCode: Int)
    case url(URLError?)
    case parsing(DecodingError?)
    case unknown
    
    var localizedDescription: String {
        switch self {
        case .badURL, .parsing, .unknown:
                return "Sorry, something went wrong."
            case .badResponse(_):
                return "Sorry, connection to our server failed."
            case .url(let error):
                return error?.localizedDescription ?? "Something went wrong."
        }
    }
    
    var description: String {
        switch self {
            case .unknown:
                return "Unknown error."
            case .badURL:
                return "Invalid URL."
            case .parsing(let error):
                return "Parsing error \(error?.localizedDescription ?? "")"
            case .badResponse(statusCode: let statusCode):
                return "Bad response with status code \(statusCode)"
            case .url(let error):
                return error?.localizedDescription ?? "url session error."
        }
    }

}

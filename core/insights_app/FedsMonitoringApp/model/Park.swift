//
//  ParkModel.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/9/23.
//

import Foundation

struct Park: Identifiable, Decodable, CustomStringConvertible {
    let id: Int
    let name: String
    let park_map: String
    let park_image: String
    let county: String
    let fire_detected: Bool
    let system_up: Bool
    
    
    var description: String {
        return "Id: \(self.id)"
    }    
}

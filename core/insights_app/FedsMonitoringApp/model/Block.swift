//
//  Block.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/10/23.
//

import Foundation

struct Block: Identifiable, Decodable, CustomStringConvertible {
    let id: Int
    let latitude: Int
    let longitude: Int
    let time_in_millis: Int64
    let url: String
    let is_detected: Bool
    var status: String
    
    var description: String {
        return "Id: \(self.id)"
    }
}

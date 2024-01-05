//
//  NetworkStatus.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/22/23.
//

import Foundation

struct NetworkStatus: Identifiable, Decodable, CustomStringConvertible {
    let id: Int
    let connectivity_flag: Bool
    
    var description: String {
        return "Id: \(self.id)"
    }
}

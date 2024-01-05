//
//  ScoutStatus.swift
//  FedsMonitoringApp
//
//  Created by Jagdish Patel on 3/18/23.
//

import Foundation

struct ScoutStatus: Identifiable, Decodable, CustomStringConvertible {
    let id: Int
    let navigate_flag: Bool
    
    var description: String {
        return "Id: \(self.id)"
    }
}

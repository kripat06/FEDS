//
//  FedsStatus.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/24/23.
//

import Foundation

struct FedsStatus: Identifiable, Decodable, CustomStringConvertible {
    let id: Int
    let offline_mode: Bool
    
    var description: String {
        return "Id: \(self.id)"
    }
}

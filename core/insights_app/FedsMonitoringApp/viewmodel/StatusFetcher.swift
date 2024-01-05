//
//  ScoutStateFetcher.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/18/23.
//

import Foundation

class StatusFetcher: ObservableObject {
    
    @Published var scoutStatus: ScoutStatus = ScoutStatus(id: 1, navigate_flag: false)
    @Published var networkStatus: NetworkStatus = NetworkStatus(id: 1, connectivity_flag: true)
    @Published var fedsStatus: FedsStatus = FedsStatus(id: 1, offline_mode: false)

    private let service = APIService()
    
    func fetchScoutStatus() {
        service.fetchScoutStatus() { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let status):
                    self.scoutStatus = status
                case .failure(let error):
                    print("Could not load: \(error)")
                }
            }
        }
    }
        
    func fetchFedsStatus() {
        service.fetchFedsStatus() { result in
            DispatchQueue.main.async {
                switch result {
                    case .success(let status):
                    self.fedsStatus = status
                    case .failure(let error):
                        print("Could not load: \(error)")
                }
            }
        }
    }

    func fetchNetworkStatus() {
        service.fetchNetworkStatus() { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let status):
                    self.networkStatus = status
                case .failure(let error):
                    print("Could not load: \(error)")
                }
            }
        }
    }
    
}

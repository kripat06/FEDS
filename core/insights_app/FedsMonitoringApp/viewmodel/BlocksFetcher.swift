//
//  BlocksForParkViewModel.swift
//  FedsMonitoringApp
//
//  Created by Krish Patel on 3/10/23.
//

import Foundation

class BlocksFetcher: ObservableObject {
    @Published var blocks:[Block] = [Block]()
    private let service = APIService()
    
    func fetchBlocks(for parkId: Int) {
        service.fetchBlocks(for: parkId) { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let blocks):
                    self.blocks = blocks
                case .failure(let error):
                    print("Could not load: \(error)")
                }
            }
        }
    }
}

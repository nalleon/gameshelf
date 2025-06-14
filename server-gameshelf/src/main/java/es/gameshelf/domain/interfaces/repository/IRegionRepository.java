package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Region;

import java.util.List;

public interface IRegionRepository {
    Region save(Region region);
    List<Region> findAll();
    Region findById(Integer id);
    Region findByName(String name);
    boolean delete(Integer id);
    Region update(Region region);
}

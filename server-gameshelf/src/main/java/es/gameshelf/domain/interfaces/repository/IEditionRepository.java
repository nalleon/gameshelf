package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Edition;

import java.util.List;

public interface IEditionRepository {
    Edition save(Edition edition);
    List<Edition> findAll();
    Edition findById(Integer id);
    Edition findByName(String name);
    boolean delete(Integer id);
    Edition update(Edition edition);
}
